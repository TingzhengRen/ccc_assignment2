import couchdb
import json

# authentication
admin = 'tr'
password = 'gg'
url = f'http://{admin}:{password}@172.26.134.244:5984/'

# get couchdb instance
couch = couchdb.Server(url)

# indicate the db name
db_name = 'city_geo'

# if not exist, create one
if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]

# data to be stored
with open('city_geo_data.json', 'r') as f:
    data = json.load(f)

for feature in data['features']:
    db[feature['id']] = feature