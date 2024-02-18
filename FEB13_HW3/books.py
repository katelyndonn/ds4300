from pymongo import MongoClient
import json
import pprint as pp

# create a client
client = MongoClient()

# establish your database connection
db = client['books']

# define collection
books_data = db.data
books_data.drop()

# read in json
with open('books.json') as file:
   file_data = json.load(file)

if isinstance(file_data, list):
    books_data.insert_many(file_data)
else:
    books_data.insert_one(file_data)

# query 1
# what fiction books have 5-star reviews and more than 5 books in stock?
# filters and excludes title and description
fiction5 = books_data.find({
    'category': 'fiction',
    'availability': {'$gt': 5},
    'stars': 5
}, {
    'title': 0,
    'description': 0
})

# avail = [pp.pprint(books) for books in fiction5[:5]
# avail

# query 2
# What are 5 books that are young adult OR cost less than or equal to $10?
# filters and excludes title and description
ya = books_data.find({
    '$or': [{
        'category': 'young adult'
    },
        {
        'price_incl_tax': {'$lte': 10.0}
    }]
},
    {
        'title': 0,
        'description': 0
    }
)

# ya_or_10 = [pp.pprint(books) for books in ya[:5]]
# ya_or_10

# query 3
# What are 5 books that are NOT in the default, classics, or mystery category, sorted by stars?
# filters and excludes title and description
myst = books_data.find({
    'category': {'$ne': ['default', 'classics', 'mystery']}
},
    {
        'title': 0,
        'description': 0
    }
).sort('stars', -1)

myst5 = [pp.pprint(books) for books in myst[:5]]
myst5