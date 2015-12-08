# Week 2 CRUD and Administrative Commands

Document limit = 16MB


### Create

    db.collection.insert(<document>)
    db.collection.insert([<document>, <document> ... ])


### Update

    db.collection.update(<where>, <doc or partial update expression>, <upsert>, <multi>)
upsert and multi are optional and false by default  
upsert - update or insert if not present

#### Update types:
- full update doc update/replacement
- partial update


    db.users.update({active: true}, {$inc: {priority: 2}}, false, true)
    db.pageviews.update({_id: "/sports/football"}, {$inc: {views: 1}}, true)

### Remove

    db.collection.remove(<expression>)
    db.collection.remove({x: 1})
    db.collection.remove({x: /ello/}) - regex

### Bulk Write Operations (ordered or unordered)

    var bulk = db.items.initializeUnorderedBulkOp(); or ...initializeOrderedBulkOp()
    bulk.insert({x: 1})
    bulk.insert({x: 2})
    bulk.execute()



#### Basic building blocks of the wire protocol:
- insert
- update
- getmore
- query
- remove


### [Database Commands](https://docs.mongodb.org/master/reference/command/)


### [Collection Methods](https://docs.mongodb.org/manual/reference/method/js-collection/)

    db.collection.stats()
    db.collection.drop()

### [Database Methods](https://docs.mongodb.org/manual/reference/method/js-database/)

    db.getLastError()
    db.runCommand({getLastError: 1, w:3, wtimeout: 5})
    db.currentOp()
    db.killOp()
