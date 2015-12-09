# Week 4 Replication

Replication - redundant copies across multiple machines. replicas/copies/backups

Replica set - replication cluster

Replication factor (RF) - number of members in replica set

Rule of thumb - no even number of members in replica sets.  add arbiter (see week 5)

Why do we use replica sets?
- HA
- data safety (durability)
- scaling (in some situations)
- disaster recovery

Replication
- Replication is asynchronous.  Designed to work on commodity servers and commodity networks, LAN and WAN.
- single primary (NOT master master)
- statement based (not binary replication).  logical/statement level vs. raw data.  Statement executed on primary is translated to one statement per affected document to be executed on secondaries.  Ex. db.foo.remove({age:30}) removes 100 documents.  The primary executes the statement, the secondaries execute 100 delete statements, one per affected document

Replica sets
- automatic failover
- automatic node recovery after a failover occurred

writes -> primary  
reads -> primary or secondary

#### Election
Election occurs when there’s a consensus (majority) the primary is down.  Member which is the most caught up generally wins and becomes new primary.  Failover takes 10's of seconds.  Drivers are replica set aware and can handle failover

#### Recovery

If the primary fails with uncommitted writes, they (uncommitted writes) are rolled back and archived when it comes back online and syncs.  A rollback directory is created where a BSON file is written containing the uncommitted writes.  See [bsondump](https://docs.mongodb.org/manual/reference/program/bsondump/) utility.

Once a cluster-wide commit is ack'd, it cannot be rolled back


### Starting a Replica Set

Replica set name is used to reduce confusion and human error.

    mongod --port 27001 --replSet abc --dbpath 1 --logpath 1/mongod.log --logappend --oplogSize 50 --smallfiles --fork
    mongod --port 27002 --replSet abc --dbpath 2 --logpath 2/mongod.log --logappend --oplogSize 50 --smallfiles --fork
    mongod --port 27003 --replSet abc --dbpath 3 --logpath 3/mongod.log --logappend --oplogSize 50 --smallfiles --fork

Initiating the set:
- specify config
- initial data - only the member that gets the initiate command can have initial data

Best practices:
- don't use raw ip addresses
- don't use names from /etc/hosts
- use DNS.  pick appropriate DNS TTL for failover considerations.  few minutes

[Replication Methods](https://docs.mongodb.org/manual/reference/method/js-replication/)

````cfg = {_id: "<replSet>", members[{_id: 0, host: "<hostname>:<port>", ...}]}````

    mongo --port 27001
    > cfg = {_id: "abc", members[{_id: 0, host:"ubuntu-pc:27001"}, {_id: 1, host: "ubuntu-pc:27001"}, {_id: 2, host: "ubuntu-pc:27003"}]}
    > rs.initiate(cfg)
    abc:PRIMARY> rs.conf()
    abc:PRIMARY> rs.isMaster()
    abc:PRIMARY> rs.status()
    abc:PRIMARY> rs.help()
    abc:PRIMARY> rs.stepDown()

### Read Preference

Cannot read from secondary unless we explicitly declare that we're ok with having eventually consistent read semantics.

    abc:SECONDARY> rs.slaveOk()

Drivers use read preference.  Data is potentially stale if reading from secondary.  "Eventually consistent"

Why query secondary?
- geography
- separate a workload (analytics server)
- separate load
- availability

Read Preference Options
1. primary (default)
2. primary preferred
3. secondary
4. secondary preferred
5. nearest

primary = 1  
primary is possible = 2, 4, 5  
secondary is possible = 2, 3, 4, 5

Rules of thumb:  When in doubt, use primary.  When remote, use nearest.  Use secondary for certain reporting workloads.  Even read loads, consider nearest.  Primary preferred and secondary preferred kinda crappy.