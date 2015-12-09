# Week 5 Replication Pt. 2

Run rs.reconfig(cfg) on **primary**.  Majority of voters are up required to reconfigure.

````cfg = {_id: "<replSet>", members[{_id: 0, host:"<hostname>:<port>", <options>}]}````

[replSetGetConfig](https://docs.mongodb.org/manual/reference/command/replSetGetConfig/)

#### [Options](https://docs.mongodb.org/manual/reference/replica-configuration/):

- ```arbiterOnly: <boolean>```  Arbiter is very lightweight, has **no data** (won’t vote for itself), but votes in election.  Arbiter is a voter.
  - Quiz: When might you want to use an arbiter?
    - To make an odd number of votes in the replica set.
    - To spread the replica set over more data centers.
    - To protect against network splits.

- ```priority: <number>```  Bias to be primary.  Default = 1, 0 (never primary), 0.5 can be primary if no one else is eligible.  < 0 is invalid

- ```hidden: <boolean>```  Clients have no visibility

- ```slaveDelay: <int>```  In seconds.  Must lag by delay time (can never be fresher than the delay time).  Rolling backup.  Length **must fit within window of oplog**.  Priority must be set to 0 if you're slave delayed (your data is behind).  Dwight not sure if ```hidden:true``` is automatic when slaveDelay is set
  - Quiz: which scenarios does it make sense to use slave delay?
    - Prevent against a new client application release bug.
    - Getting a view of the DB between backups.
    - During development when using experimental queries.

- ```votes: <number>```  Not recommended.  Set number of votes for a member.  As of MongoDB 3.0, a member can only have 0 or 1 votes.  Also MongoDB allows a max of 7 voting members in a replica set.  "7+ members in a replica set would be unusual."  Limit is 12 members.

Can reconfigure with a node down as long as you have a majority.

Cluster Wide Commits Principles
- write is truly committed upon application at a majority of the set.  Durable.
- We can get ack of #1

[getLastError](http://docs.mongodb.org/manual/reference/command/getLastError/)

    db.foo.insert({x:3})
    db.getLastError({w: "majority", wtimeout: 300})

Best not to use a number for w since the replica set can change.  Also, set a wtimeout if you specify w to avoid blocking indefinitely.  wtimeout is in *milliseconds*.


### [Write Concern](https://docs.mongodb.org/manual/reference/write-concern/)
1. no call to getLastError. Use case: increment page view, logging
2. w: 1  Use case: not super critical, no duplicate key issue
3. w: 'majority' Use case: Most/important things
4. w:3 (all) Use case: if RF=3, flow control (all servers caught up)
5. w: tag

“Call every n” - bunch of inserts, check every nth (with getLastError)
Can make a series of calls then call GLE; first call, GLE, bunch more calls, GLE

Good practices:
- use write concern
- use majority
- tune iff slow
- call GLE when job ends

Quiz: Does getLastError() need to be called if using default write concerns? No

Batch inserts - example:

    db.m102.insert([{"a": 1}, {"b": 2}, {"c": 3}])

(didn’t really cover this)

Connection pile-up on slowness.  Choose number of connections carefully, choose wtimeout carefully, monitor for lag.

Quiz: What are some issues with using wtimeout?
- a write can be made but getLastError() could report a failure.
- each query could potentially take the full duration of the wtimeout
- pile-ups of connections

### Data Center

1 Data Center
- 3 members (common case)
- 2 + arbiter
- 2 with manual failover
- 5 members (??)
- 2 large + 1 small (?)

Multi DC (some options)
- Primary, Secondary, and other secondary all in separate DC’s
- Primary, Secondary, and Arbiter in separate DC’s

#### Mixed Storage Engine Replica Sets
Why?  Testing, upgrading.  Replication sends ops from primary, not bytes.

