# Week 7 Backup and Recovery

Security
- "trusted environment" - no one has access except for clients (and they get full access to db).  lock down @ network layer, relevant tcp ports.  Default.
- mongodb authentication --auth (securing client access- authentication and authorization) --keyFile fname (intra-cluster authentication).  Can layer ssl atop (encryption of all communications) but have to compile mongo with scons --ssl option

keyFile for intracluster authentication (members of shard/replica sets).  shared secret key file to cross authentication among themselves to coordinate their actions.  file present on all servers in cluster.

Data between clients and cluster and members of cluster is unencrypted.  Initial authentication handshake is **secure.**

- authentication (mongodb challenge/response, X.509/SSL certs, kerberos*, ldap*)
- access control / authorization
- encryption
- network setup
- auditing*

*= non free edition.  enterprise.


    mongod --auth --keyfile <fname>
    mongos --auth --keyfile <fname>

users and roles for that db: ```<dbname>.system.users```

admin db is special - users and roles that are cluster/server wide


    var me = {user:"dwight", pwd:"asdf", roles:["userAdminAnyDatabase"]}
    db.createUser(me)
    mongo localhost/admin -u dwight -p asdf

(leave off passwd to get prompted)

### [Built-In Roles](https://docs.mongodb.org/v3.0/reference/built-in-roles/)

#### Database User Roles
- read
- readWrite

#### Database Administration Roles
- dbAdmin
- dbOwner
- userAdmin

#### Cluster Administration Roles
- clusterAdmin
- clusterManager
- clusterMonitor
- hostManager

#### All-Database Roles

- readAnyDatabase
- readWriteAnyDatabase
- userAdminAnyDatabase
- dbAdminAnyDatabase


```mongo --host localhost```  
```db.addUser("the_admin", "testpassword")```

User Types
- admin - can do administration, created in the admin db, can access all databases
- regular - access specific db, read/write or readOnly

```db.createUser(<user>, <pswd>, [<readOnly>])```

contents of keyfile a string of base64 legal characters

    # touch keyfile
    # chmod 600 keyfile
    # openssl rand --base64 60

### Backup and Restore
- [mongodump](https://docs.mongodb.org/manual/reference/program/mongodump/) --oplog, [mongorestore](https://docs.mongodb.org/manual/reference/program/mongorestore/) --oplogReplay.  oplog option for real "point in time" backup.  Hot backup (doesn't need to be shutdown)
- filesystem snapshot.  lvm?  hot backup.  **Must** have journaling enabled.  db.fsyncLock() / fsyncUnlock() - db snapshots of sub-volumes.  Needs to be quick since no reading/writing during the lock.
- backup from secondary - shutdown, copy files, restart.  start back up and it will catch up

### Backup a Sharded Cluster
1. Turn off balancer during backup of sharded cluster.  ```sh.stopBalancer()```
2. Backup config db.  ```mongodump --db config```.  Or could stop one of 3 config server then copy its files.
3. Backup each shard’s replica set.  One healthy member (and not lagging) that has data from each shard.  Not a point in time backup.  Not a snapshot of the whole cluster.
4. ```sh.startBalancer()```

Restore: Shutdown everything, restore files to proper locations, restart.

    mongodump --host some_mongos_or_some_config_server --db config


Example:

    mongo --host some_mongos --eval "sh.stopBalancer()"
    mongodump --host some_mongos_or_some_config_server --db config /backups/cluster1/configdb
    mongodump --host shard1_svr --oplog /backups/cluster1/shard1
    mongodump --host shard2_svr --oplog /backups/cluster1/shard2
    mongodump --host shard3_svr --oplog /backups/cluster1/shard3
    mongodump --host shard4_svr --oplog /backups/cluster1/shard4
    mongodump --host shard5_svr --oplog /backups/cluster1/shard5
    mongodump --host shard6_svr --oplog /backups/cluster1/shard6
    mongo --host some_mongos --eval "sh.startBalancer()"


### Additional Features

Capped Collections
- circular queues
- least recently inserted order
- preallocated max size
- cannot delete or grow

TTL Collections (v2.2+) - introduced in Week 3
- auto age-out of old documents
- creating special index

[GridFS](https://docs.mongodb.org/manual/core/gridfs/) (grid file system) - store files in mongodb.  BSON size limit 16MB.  convention for chunking large/huge data files or binary objects.  Large BLOB storage.  Predefined specs.  utility: [mongofiles](https://docs.mongodb.org/manual/reference/program/mongofiles/#bin.mongofiles)

[Production Notes](http://docs.mongodb.org/master/administration/production-notes/)

Hardware Tips (+ software)
- bias towards faster cpu core vs. more cores
- RAM is good
- 64 bit
- virtualization is 'ok' but not required
- disable [NUMA](https://en.wikipedia.org/wiki/Non-uniform_memory_access)
- SSDs are good, ‘wear endurance’, reserve empty space (unpartitioned) ~20%
- file system cache is most of mongod’s memory usage
- check readahead setting! (small value).  blockdev --report

Additional MongoDB Resources
- [Manual](https://docs.mongodb.org/manual/)
- [Drivers](http://docs.mongodb.org/ecosystem/drivers/)
- [bug database, features](https://jira.mongodb.org/secure/Dashboard.jspa)
- [Google Groups](https://groups.google.com/forum/#!forum/mongodb-user)
- IRC freenode.net/#mongodb
- [Github](https://github.com/mongodb/mongo)
- [Blog](http://blog.mongodb.org/)
- [Twitter](https://twitter.com/MongoDB)
- meetup groups
- mongo monitoring service
