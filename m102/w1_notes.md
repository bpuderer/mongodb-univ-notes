# Week 1 - Introduction

#### Concepts and Rationale, Why use MongoDB:
- hardware - parralelism, commodity servers/networks, cloud
- scale up, big data
- make app development easier and elegant (complex structure, unstructured, polymorphic)

MongoDB tries to hit the sweet spot of features and scale + speed.  Too many features and can't scale.

Document oriented, data stored together not broken apart

JSON - flexible and concise framework for specifying queries as well as storing records, syntax resembles common data structures in many languages, language independent

Types in [JSON](http://www.json.org/): string, number, Boolean, null, arrays, objects  

#### Why does MongoDB use [BSON](http://bsonspec.org/)?
- fast scannability/access (field sizes are part of BSON)
- data types (data type, binary data, object id)

Client uses a driver to go from BSON to representation that makes sense in the programming language.  "Serialization format"

MongoDB - dynamic schema, not really [schemaless](http://blog.mongodb.org/post/119945109/why-schemaless) --> flexibility iteration/agile, data representation polymorphic

#### Document _id field:
- automatically created for document if not specified
- can be any type but must be unique within collection
- immutable.  Does not change over the lifetime of the document
- automatically indexed

Start [mongod](https://docs.mongodb.org/manual/reference/program/mongod/) daemon:

    mongod --port 27001 --dbpath data --smallfiles --fork --logappend --logpath data/mongod.log

mongod default path = `/data/db`  
if config server (--configsvr), `/data/configdb`

    mongoimport --stopOnError --db pcat --collection products < products.json

[mongoimport](https://docs.mongodb.org/v3.0/reference/program/mongoimport/) can import JSON, CSV, and TSV formats

#### Data directory:
- journal - redo logs for crash recovery
- pcat.n - data files, auto-created, pre-allocated up to 2GB in size
- pcat.ns - 'system catalog', ns = namespace

[mongo](https://docs.mongodb.org/getting-started/shell/client/) shell uses the "test" database by default

db - predefined variable with connection to database

    show dbs
    use <database>
    show collections
    db.<collection>.count()
    db.<collection>.find()
    db.<collection>.findOne()
    db.<collection>.find().limit(4).skip(2).toArray()

`db.<collection>.find()` returns a cursor to the results and iterates up to 20 times to access up to the first 20 docs that match the query
it - iterate the [cursor](https://docs.mongodb.org/manual/reference/method/js-cursor/), get 20 more, Type "it" for more

[Query expressions](https://docs.mongodb.org/manual/reference/operator/query/) are Boolean ands.  If a field is an array it is interpreted as being in the array.  Can use dot notation for field name in query expression and requires quotes (around field name).

[Projection document](https://docs.mongodb.org/manual/tutorial/project-fields-from-query-results/) limits fields in returned documents.  _id must be explicitly suppressed as it is included by default.

    db.collection.find( <query expression>, <projection/field selection> )
    db.collection.find({}, {name: 1, _id: 0})
    db.collection.find({price: {$gte: 200}}, {name: 1, price: 1})

sort criteria - `{<field>: <direction>}` 1 = ascending, -1 = descending

    db.find().sort({name: 1})

