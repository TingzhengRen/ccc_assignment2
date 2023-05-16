from flask import Flask, render_template, request
from flask_restful import Api
from flask_cors import CORS
import nltk
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from collections import defaultdict

import couchdb

# admin and password
admin = 'tr'
password = 'gg'
# url address to visit couchdb
url = f'http://{admin}:{password}@172.26.134.244:5984/'

# get couchdb instance
couch = couchdb.Server(url)

# identify the database name
db_name1 = 'mastodon'
# get the database
db1 = couch[db_name1]

# 
app = Flask(__name__)
api = Api(app)
CORS(app)



def extract_useful_info(text):
    # 解析HTML文本
    soup = BeautifulSoup(text, 'html.parser')

    # 提取纯文本
    plain_text = soup.get_text()

    # 分割成单词
    words = plain_text.split()

    # 统计词频
    word_counts = defaultdict(int)
    for word in words:
        word_counts[word] += 1

    return dict(word_counts)


@app.route('/api_0/<param>')
def api_0(param):
    # find the data
    query = {
        'selector': {
            'content': {
                
                '$regex': param
                
            }
        }
    }
    results = []
    # get the results
    for row in db1.find(query):
        results.append(extract_useful_info(row['content']))
    output = {}
    for i in range(len(results)):
        for key,value in results[i].items():
            if key in output:
                output[key] = output[key]+1
            else:
                output[key] = 1
    stop_words = set(stopwords.words('english'))
    filtered_dict = {k: v for k, v in output.items() if k not in stop_words}
    converted_list = [{"key": k, "value": v} for k, v in filtered_dict.items()]


    # output the results
    return {'data': converted_list}

db_name2 = 'twitter_vic'
# get the database
db2 = couch[db_name2]

@app.route('/api_1/1')
def api_1():
    query = {
        'selector': {
            'city': {
                
                '$exists': True
                
            }
        }
    }
    results = []
    for row in db2.find(query):
        if row['city'] != None:
            results.append(row['city'])
    count = {}
    for i in range(len(results)):
        if results[i] in count:
            count[results[i]] = count[results[i]]+1
        else:
            count[results[i]] = 1
    return {'data': count}

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='8080')
