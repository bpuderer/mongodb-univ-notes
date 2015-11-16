db.zips.aggregate([
    {$group: {_id: {city: "$city", state: "$state"}, pop: {$sum: "$pop"}}},
    {$match: {$and: [{pop: {$gt: 25000}}, {$or: [{"_id.state": "CA"}, {"_id.state": "NY"}]}]}},
    {$group: {_id: null, average: {$avg: "$pop"}}}
])
