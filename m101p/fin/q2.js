db.messages.aggregate([
{$unwind: "$headers.To"},
{$group: {_id: "$_id", from: {$first: "$headers.From"}, to: {$addToSet: "$headers.To"}}},
{$unwind: "$to"},
{$group: {_id: {from: "$from", to: "$to"}, num: {$sum: 1}}},
{$sort: {num: -1}}
])
