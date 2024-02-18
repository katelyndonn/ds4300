from pymongo import MongoClient
import pprint as pp
import pandas as pd

# create a client
client = MongoClient()

# establish your database connection
db = client['yelp']

# define collection
yelp_data = db.data
yelp_data.drop()

# read in json
df = pd.read_json('yelp.json', lines=True)
df = df.to_dict(orient="records")
yelp_data.insert_many(df)

# query 1
# what are 5 open restaurants in Tampa, FL that have more than 20 4-star reviews?
# filters and excludes latitude, longitude, and address
tampa = yelp_data.find({
    'city': 'Tampa',
    'stars': {'$gt': 4.0},
    'is_open': 1,
    'review_count': {'$gt': 20}
}, {
    'latitude': 0,
    'longitude': 0,
    'address': 0
})

# florida = [pp.pprint(restaurant) for restaurant in tampa[:5]]
# florida

# query 2
# What are 5 restaurants that are Tim Hortons OR are in postal code 19124?
tim = yelp_data.find({
    '$or': [{
        'name': 'Tim Hortons'
    },
        {
        'postal_code': 19124
    }]
})

# tim_or = [pp.pprint(restaurant) for restaurant in tim[:5]]
# tim_or

# query 3
# What are 5 restaurants that offer bike parking and are wheelchair accessible, sorted by stars?
amenities = yelp_data.find({
    'attributes': {'BikeParking': 'True',
                   'WheelchairAccessible': 'True'}
}
).sort('stars', -1)

amen = [pp.pprint(restaurant) for restaurant in amenities[:5]]
amen