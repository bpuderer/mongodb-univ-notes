import pymongo

connection = pymongo.MongoClient("mongodb://localhost")
db = connection.q7

print "images tagged 'kittens' before removing orphans:", db.images.find({'tags': 'kittens'}).count()

print "deleting orphans..."

cursor = db.images.find({})

num_images_deleted = 0
for c in cursor:
    image_id = c['_id']
    album = db.albums.find_one({'images': image_id})

    if not album:
        result = db.images.delete_one({'_id': image_id})
        num_images_deleted += result.deleted_count

print "purged", num_images_deleted, "images"

print "images tagged 'kittens' after removing orphans:", db.images.find({'tags': 'kittens'}).count()
