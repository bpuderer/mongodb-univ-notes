import pymongo

connection = pymongo.MongoClient("mongodb://localhost")
db = connection.school

cursor = db.students.find({})

for c in cursor:
    hw_grade_to_remove = 0
    first_homework = True
    for score in c['scores']:
        if (score['type'] == "homework") and first_homework:
            #first homework
            hw_grade_to_remove = score['score']
            first_homework = False
        elif (score['type'] == "homework") and score['score'] < hw_grade_to_remove:
            #second homework and less than first
            hw_grade_to_remove = score['score']

    print "Homework to remove:", hw_grade_to_remove

    db.students.update_one({'_id': c['_id']}, {'$pull': {'scores': {'score': hw_grade_to_remove, 'type': "homework"}}})

