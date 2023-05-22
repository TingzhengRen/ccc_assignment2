from flask import Flask
from flask_restful import Api
from flask_cors import CORS
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
        }
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
        }
    }
    results = []
    for row in db4.find(query):
        results.append((row['properties'],row['geometry']))
    return {'data': results}

db_name5 = 'sudo'
# get the database
db5 = couch[db_name5]

def extract_number(key):
    # 从键中提取数字部分
    return int(''.join(filter(str.isdigit, key)))

def extract_numbers(items):
    numbers_only = []
    for item in items:
        if isinstance(item, (int, float)):
            numbers_only.append(item)
        elif isinstance(item, str):
            try:
                number = float(item)
                numbers_only.append(number)
            except ValueError:
                # Ignore non-numeric values
                pass
    return numbers_only


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
        f_keys_to_extract.extend((key, properties[key]) for key in properties.keys() if 'income' in key and key.startswith('f_'))
        m_keys_to_extract.extend((key, properties[key]) for key in properties.keys() if 'income' in key and key.startswith('m_'))

    f_sorted_list = sorted(f_keys_to_extract, key=lambda x: int(''.join(filter(str.isdigit, x[0]))))
    m_sorted_list = sorted(m_keys_to_extract, key=lambda x: int(''.join(filter(str.isdigit, x[0]))))

    list_1 = [item for i, item in enumerate(f_sorted_list) if i % 2 == 0]
    list_2 = [item for i, item in enumerate(f_sorted_list) if i % 2 == 1]
    list_3 = [item for i, item in enumerate(m_sorted_list) if i % 2 == 0]
    list_4 = [item for i, item in enumerate(m_sorted_list) if i % 2 == 1]

    list_1_numbers = extract_numbers([item[1] for item in list_1])
    list_2_numbers = extract_numbers([item[1] for item in list_2])
    list_3_numbers = extract_numbers([item[1] for item in list_3])
    list_4_numbers = extract_numbers([item[1] for item in list_4])



    return {'data': [list_1_numbers,list_2_numbers,list_3_numbers,list_4_numbers]}




if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='8080')
