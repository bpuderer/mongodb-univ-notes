# Week 6 Scalability

shards - partition

a given BSON document will live on one and only one shard at a given point in time.  Each shard has different data (partitioned)

sharding for scale out

distribution is based on a "shard key", documents with same shard key are on the same shard

shard key ranges [K(l), K(h)] for a given shard (shard key low, shard key high)

docs in the same collection which share the same shard key all on same shard.  in addition docs whose shard key is close to the other shard key in sort order will tend to be on the same shard too - "range-based partitioning"

['jane', 'joe'] -> S0  
['joe', 'kyle'] -> S2

why range based?
1. efficiency for queries that involve ranges.  send queries to particular shards
2. useful for sorting

More shards, higher replication factor

data/documents in a range is referred to as a "chunk", ~100MB each

Background operations (even distribution of data across shards)
- split - split a chunk into 2 chunks. joe-kyle -> joe-kate, kate-kyle.  cheap and lightweight
- migrate - maintain balance across shards.  moves data from shard to shard.  more expensive.  data still live during migration.  [balancer](https://docs.mongodb.org/manual/tutorial/manage-sharded-cluster-balancer/) - decides when to do migrations and where.  balances on number of chunks.


[Config Server](https://docs.mongodb.org/manual/core/sharded-cluster-config-servers/) - small mongod storing metadata (about chunks and system).  metadata store.  **Three in a production environment.**  identical data and are sync'd.  

if any of config servers go down, splits and migrates cannot happen.  reading is fine.  cluster only goes down if all go down.

[mongos](https://docs.mongodb.org/manual/reference/program/mongos/) - clients connect to mongos to perform operations on cluster.  provides the client a view of the cluster as a single logical entity.  no persistent state.

mongod - data stores / database (same as before)

Config server (3x):

    mongod --configsvr --dbpath <path> --port <port> --fork --logpath <log> --logappend

Shard server (default port with shardsvr is 27018)

    mongod --shardsvr --replSet <repl set name> --dbpath <path> --logpath <log> --port <port> --fork --logappend --smallfiles --oplogSize 50

Example mongos (several of these, can place on client, can place on every member of replica set.  default port 27017):

    mongos --configdb 10gen.local:26050,10gen.local:26051,10gen.local:26052 --fork --logappend --logpath log.mongos0

Run mongos on the standard tcp port 27017.  Do not run shard server mongod’s or config servers on that port.  Clients should connect on 27017.

Don’t have to connect directly to config database to access it.  ```use config```

For each shard:

- initiate the replica set 
  - rs.initiate()
  - rs.add("name:port")
  - rs.status()
- "add" the shard to the cluster.  ```sh.addShard("replset/name:port")```  name:port of one member of replica set...it’ll find other members of replica set.  ```sh.status()```

Unsharded collections reside fully on the primary/first shard (shard0) of the cluster.

[Sharding Commands](https://docs.mongodb.org/manual/reference/command/nav-sharding/)

### Sharding a collection

NOTE: to shard a collection, you must have an index on the shard key so create the index first.

    mongos> sh.enableSharding("<database>")

partitioned: true (means sharding enabled for db)

    mongos> sh.shardCollection("<database>.<collection>", key, unique)

**key** is the index spec doc to use as the shard key.  **unique** is a boolean which enforces a unique constraint.  Example:

    mongos> sh.shardCollection("week6.foo", {_id: 1}, true)
    mongos> sh.status(verbose: true)

Inserts fail if they don’t include shard key

"targeted query" - uses shard key, only hits minimal number of shards

"scatter gather query" - every shard has to be hit

Quiz: "The queries that use either the shard key, or a shard key prefix, are not scatter gather.  They will be targeted only at those shards that contain the documents that will be returned by the query."

#### [Shard key selection](https://docs.mongodb.org/manual/tutorial/choose-a-shard-key/)
- the shard key is common in queries for the collection
- good cardinality / granularity
- consider compound shard keys
- is the key monotonically increasing? (ex. timestamps, BSON object id’s...insertion load not spread out)

Quiz: Generally speaking, shard keys with non-uniform key distributions are: OK.  No assumption of uniformity of shard key distribution in the design of the sharding.

#### [Pre-splitting](https://docs.mongodb.org/manual/reference/method/sh.splitAt/)
Often don't need to pre-split (specify initial key range), but you can manually do it in the shell if it's getting loaded faster than it can migrate out

    mongos> sh.splitAt("<database>.<collection>", query)

#### Sharding best practices
- only shard big collections
- pick shard keys carefully, they aren’t easily changeable
- consider pre-splitting on a bulk load
- be aware of monotonically increasing shard key values on inserts
- adding shards is fairly easy but takes time
- always connect to mongos except for some dba work.  put mongos on default port 27017, keep non-mongos processes off of 27017
- use logical names for config servers.  read docs if changing config servers
