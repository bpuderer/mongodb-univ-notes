db.grades.aggregate([
    {$unwind: "$scores"},
    {$match: {"scores.type": {$ne: "quiz"}}},
    {$group: {_id: {student_id: "$student_id", class_id: "$class_id"}, average: {$avg: "$scores.score"}}}, 
    {$group: {_id: {class_id: "$_id.class_id"}, average: {$avg: "$average"}}},
    {$sort: {average: -1}}
])
