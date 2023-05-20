import couchdb
import json

# authentication
admin = 'tr'
password = 'gg'
url = f'http://{admin}:{password}@172.26.134.244:5984/'

# get couchdb instance
couch = couchdb.Server(url)

# indicate the db name
db_name = 'vic_all'

# if not exist, create one
if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]

# data to be stored
with open('vic_all.json', 'r') as f:
    data = json.load(f)

# assume data is a list of dicts
for i, item in enumerate(data):
    # define the _id
    my_id = f'my_id_{i}'
    item['_id'] = my_id

    if db.get(my_id):
        # if the document already exists, we need to include its current _rev field
        item['_rev'] = db.get(my_id).rev

    # save to db
    doc_id, doc_rev = db.save(item)
    print(f"Document saved with ID: {doc_id} and revision: {doc_rev}")

# basic query all the docs
for _id in db:
    doc = db.get(_id)
    # filter and do sth
    print(f"ID: {_id}, Rev: {doc['_rev']}")
