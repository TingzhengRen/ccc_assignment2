### Xinyi Rui - 1135819 - xrrui@student.unimelb.edu.au
### Wenxin Zhu - 1136510 - wenxin2@student.unimelb.edu.au
### Tingzheng Ren - 1287032 - tingzhengr@student.unimelb.edu.au
### Shiqi Liang - 1420147 - liasl1@student.unimelb.edu.au
### Jingchen Shi - 1135824 - jingchens1@student.unimelb.edu.au


import couchdb
from mastodon import Mastodon, StreamListener
import json
import time

# define the log-in information details
admin = 'uki'
password = '15123'
url = f'http://{admin}:{password}@172.26.134.244:5984/'

# get to couchdb
couch = couchdb.Server(url)

db_name = 'mastodon'

# create a new data base as difined above if not exist
if db_name not in couch:
    db = couch.create(db.name)
else:
    db = couch[db_name]

# define the header of accessing Mastodon (attach token)
def header(server_name,token):
    m = Mastodon(
        api_base_url = 'https://mastodon.{}'.format(server_name),
        access_token = token)
    return m

# crawling per toot (real time) in the server and save in the couchdb with (ID, revision)
class Listener(StreamListener):
    def on_update(self, status):
        json_str = json.dumps(status, indent=2, sort_keys=True, default=str)
        doc_id, doc_rev = db.save(json.loads(json_str))
        print(f'Document saved with ID: {doc_id} and revision: {doc_rev}')



# define the time
import datetime
import threading

# Attempt 1: try to set a timer to collect Mastodon data regularly
#def timer():
 #   now_time = datetime.datetime.now()
  #  next_time = datetime.datetime.strptime(str(next_year) + "-" + str(next_month) + "-" + str(next_day) + " 15:44:00", "%Y-%m-%d %H:%M:%S")
   # timer_start_time = (next_time - now_time).total_seconds()
    #timer = threading.Timer(3600, header("world", "YEq8LisNIoIWWQaHgxI6iNJv4kVrrLH0gK7-rkAOzNE").stream_public(Listener()))
    #timer.start()


# Attempt 2: define the multi-threading tasks to implement data crawling to improve efficiency
import datetime
import schedule
import threading
import time

def job1(): # au server
    print("I'm working for job1 start", datetime.datetime.now())
    header("au","aIRrNQIn-JTuX3lS6EqOaQ2dbL25sGAgZKnjetUZ5go").stream_public(Listener())
    time.sleep(2)
    print("job1: end", datetime.datetime.now())

def job2(): # world server
    print("I'm working for job2 start", datetime.datetime.now())
    header("world", "YEq8LisNIoIWWQaHgxI6iNJv4kVrrLH0gK7-rkAOzNE").stream_public(Listener())
    time.sleep(2)
    print("job2: end", datetime.datetime.now())

def job1_task():
    threading.Thread(target=job1).start()

def job2_task():
    threading.Thread(target=job2).start()

def run():
    schedule.every(3).seconds.do(job1_task)
    schedule.every(3).seconds.do(job2_task)

    while True: # stop for 1 secend to reduce the stress of Mastodon website
        schedule.run_pending()
        time.sleep(1)
if __name__ == '__main__':
    run()






