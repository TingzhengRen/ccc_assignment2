### Xinyi Rui - 1135819 - xrrui@student.unimelb.edu.au
### Wenxin Zhu - 1136510 - wenxin2@student.unimelb.edu.au
### Tingzheng Ren - 1287032 - tingzhengr@student.unimelb.edu.au
### Shiqi Liang - 1420147 - liasl1@student.unimelb.edu.au
### Jingchen Shi - 1135824 - jingchens1@student.unimelb.edu.au



import couchdb
import json

# authentication
admin = 'tr'
password = 'gg'
url = f'http://{admin}:{password}@172.26.134.244:5984/'

# get couchdb instance
couch = couchdb.Server(url)

# indicate the db name
db_name = 'sudo'

# if not exist, create one
if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]
    
    
def read_sal(json_file):
    """
    Reads data from SUDO
    :param json_file: JSON file path
    """
    # read the json file
    try:
        with open(json_file, 'r', encoding='utf-8') as sal_file:
            sal_data = json.load(sal_file)
        return sal_data
    except (FileNotFoundError, IOError) as e:
        print(e)
        


# data to be stored
data = read_sal("C:/Users/Administrator/OneDrive/桌面/2023 S1 Coding/COMP90024 CCC/ass2/SUDO/ABS_-_Jobs_In_Australia_-_Employed_Persons_Jobs__GCCSA__2011-2018.json/abs_aus_jobs_employed_persons_jobs_gccsa_2011_2018-820249227480448152.json")

# save to db
doc_id, doc_rev = db.save(data)
print(f'Document saved with ID: {doc_id} and revision: {doc_rev}')

# define the _id
my_id = 'my_id'
print(db.get(my_id))
if db.get(my_id):
    rev = db.get(my_id).rev
    data['_id'] = my_id
    data['_rev'] = rev
else:
    data['_id'] = my_id

# save to db
doc_id, doc_rev = db.save(data)
print(f"Document saved with ID: {doc_id} and revision: {doc_rev}")

# basic query all the docs
for _id in db:
    doc = db.get(_id)
    # filter and do sth
    print(f"ID: {_id}, Rev: {doc['_rev']}")
