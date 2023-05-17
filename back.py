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
        },
        'limit': 200000
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

@app.route('/api_1/city_count')
def api_1():
    query = {
        'selector': {
            'city': {
                '$ne': None
            }
            
        },
        'limit': 200000
    }
    results = []
    for row in db2.find(query):
        results.append(row['city'])
    count = {}
    for i in range(len(results)):
        if results[i] in count:
            count[results[i]] = count[results[i]]+1
        else:
            count[results[i]] = 1
    return {'data': count}

db_name3 = 'vic_geo'
# get the database
db3 = couch[db_name3]

@app.route('/api_2/vic_geo')
def api_2():
    query = {
        "selector": {
            "_id": {"$gt": None}
        },
        'limit': 5000
    }
    results = []
    for row in db3.find(query):
        results.append((row['properties'],row['geometry']))
    return {'data': results}

db_name4 = 'city_geo'
# get the database
db4 = couch[db_name4]

@app.route('/api_3/city_geo')
def api_3():
    query = {
        "selector": {
            "_id": {"$gt": None}
        },
        'limit': 5000
    }
    results = []
    for row in db4.find(query):
        results.append((row['properties'],row['geometry']))
    return {'data': results}

db_name5 = 'sudo'
# get the database
db5 = couch[db_name5]

@app.route('/api_4/broke_line')
def api_4():
    query = {
        "selector": {
            "_id": {"$gt": None}
        },
        'limit': 5000
    }
    results = []
    for row in db5.find(query):
        results.append(row)

    # Extracting keys starting with "f_" and "m_"
    f_keys_to_extract = []
    m_keys_to_extract = []
    for feature in results[0]['features']:
        properties = feature['properties']
        f_keys_to_extract.extend(key for key in properties.keys() if 'income' in key and key.startswith('f_'))
        m_keys_to_extract.extend(key for key in properties.keys() if 'income' in key and key.startswith('m_'))

    # Accessing the values of the extracted keys
    f_extracted_values = []
    m_extracted_values = []
    for feature in results[0]['features']:
        properties = feature['properties']
        f_values = [properties[key] for key in f_keys_to_extract]
        m_values = [properties[key] for key in m_keys_to_extract]
        f_extracted_values.append(f_values)
        m_extracted_values.append(m_values)

    return {'data': [f_extracted_values, m_extracted_values]}



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='8080')
