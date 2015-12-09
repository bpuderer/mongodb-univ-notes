# Week 3 Performance

Storage engine - interface between database server and hardware it's running on.  Affects how data is written, removed, read, and structures used to store data

MongoDB 3.0 - pluggable storage engine, but only two choices, MMAPv1 and WiredTiger

### MMAPv1
- uses mmap system call which maps data files directly into virtual memory
- collection level locking in MongoDB 3.0
- multiple readers, single writer lock
- data on disk is BSON


`mongod --storageEngine mmapv1`

db.serverStatus() will show storageEngine

journal - ensures consistency of the data on disk in the event of a failure, write-ahead log, write down what you’re about to do then you do it

data files - database.n, starts at 64MB then doubles up until 2GB then allocates 2GB at a time

Power of 2 sized allocations.  Room to grow for every document.  Standardized size so hole it leaves when it moves is likely to be reused.  Documents that grow at a constant rate will move less often as time goes on.

### [WiredTiger](https://docs.mongodb.org/manual/core/wiredtiger/)

- document level locking (flagship feature in MongoDB 3.0)
- compression
  - snappy (default, fast)
  - zlib(more compression)
  - none
- performance gains in many use cases
- stores in B-trees
- writes are separate and incorporated later (during update, writes a new version instead of overwriting existing data like mmapv1.  so no document movement or padding factor)


`mongod --storageEngine wiredTiger`

WiredTiger cache = half of RAM (by default)

#### Checkpoints  
*checkpoint* ensures that the data files are consistent up to and including the last checkpoint.  MongoDB configures WiredTiger to create checkpoints every 60 seconds or 2GB of journal data.  

WT Cache -> FS Cache -> Disk  

## Indexes
- keys can be any type
- _id index is automatic (unique)
- other than _id, explicitly declared
- automatically used
- can index array contents
- can index subdocuments and subfields
- fieldnames are not in the index

Indexes are needed to avoid collection scans (table scans) - sequential scan through the whole collection = SLOW!

> An index for every query and a query for every index.

Background Index Building - bg operation on primary, fg on secondaries, slower than fg, fg packs more

Indexes can be ascending or descending, 1 or -1 respectively when created

    db.collection.createIndex({a: 1})

Compound index - index on 1+ fields, order matters

    db.collection.createIndex({a: 1, b: 1})

Unique key constraint

    db.collection.createIndex({a: 1}, {unique: true})

Option when field rarely exists

    db.collection.createIndex({a: 1}, {sparse: true})

View indexes

    db.collection.getIndexes()

Drop index - can also delete by name which can be set on creation

    db.collection.dropIndex({a: 1})

Q: If an index is created with the options document, { unique : true } can 2 documents which do not include the field that is indexed exist in the same collection? NO

Q: 
If an index is unique AND sparse, can 2 documents which do not include the field that is indexed exist in the same collection? YES

#### TTL index
index to automatically remove documents from a collection after a certain amount of time

    db.collection.createIndex({a: 1}, {expireAfterSeconds: <number>})

#### [Geospatial](https://docs.mongodb.org/manual/applications/geospatial-indexes/)
    db.collection.createIndex({loc: "2dsphere"})
    db.places.find({loc: {$near: {$geometry: {type: "Point", coordinates:[2,2.01]}, spherical: true}}})

#### [Text search](https://docs.mongodb.org/manual/reference/operator/query/text/#op._S_text)

Field that's indexed has to be a string

    db.collection.createIndex({words: "text"})

case insensitive, plurality insensitive (tree or trees matches tree)

    db.collection.find({$text: {$search: "cat"}})

search for multiple by separating with a space (logical OR)

    db.collection.find({$text: {$search: "cat tree"}}, {score:{$meta:”textScore”, _id: 0})

### Explain
return an Explainable object to see what indexes are used in a query (aggregate, find, count, remove, update, group).
- queryPlanner (default)
  - `db.example.explain().find({a: 17}).sort({b: -1})`
  - queryPlanner.winningPlan.stage - if COLLSCAN then no index was used
- executionStats - includes queryPlanner, more info (execution time, number of docs returned, docs examined)
  - `exp = db.collection.explain("executionStats")`
  - `exp.find({a: 17, b: 55})`
- allPlansExecution - like executionStats but also runs each available plan and returns stats

Covered Query - no need to touch docs, just use index. *executionStats.totalDocsExamined=0*


### [Profiler](https://docs.mongodb.org/manual/tutorial/manage-the-database-profiler/)
stats stored in system.profile collection

level 0 = off (default), 1 = only collects data for slow ops, 2 = on

    db.setProfilingLevel(<level>, <slowms>)
    db.setProfilingLevel(2)
    db.setProfilingLevel(1, 3)


mongostat --port 27001  
mongotop --port 27001  
`db.currentOp()` - returns inprog array  
`db.killOp(<opid>)`