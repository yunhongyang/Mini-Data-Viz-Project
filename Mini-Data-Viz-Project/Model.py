# train model
import pandas as pd
df = pd.read_csv('2023-04-14-job-search/Clean_Data/combined_data_final.csv')
# load packages
import numpy as np
import pandas as pd
import re
import time
from datasketch import MinHash, MinHashLSHForest
# preprocess data
def preprocess(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^\w\s]','',text)
    text = re.sub(r'\s\s+',' ',text)
    text = text.strip()
    tokens = text.lower()
    tokens = tokens.split()
    return tokens
# choose parameters - Number of Permutations
permutations = 128
# Create MinHash objects
def get_forest(data, perms):
    start_time = time.time()
    minhash = []
    for text in data['text']:
        tokens = preprocess(text)
        m = MinHash(num_perm=perms)
        for s in tokens:
            m.update(s.encode('utf8'))
        minhash.append(m) 
    forest = MinHashLSHForest(num_perm=perms)
    for i,m in enumerate(minhash):
        forest.add(i,m)  
    forest.index()
    print('It took %s seconds to build forest.' %(time.time()-start_time))
    return forest
# evaluate query
def predict(text, database, perms, num_results, forest):
    start_time = time.time()
    tokens = preprocess(text)
    m = MinHash(num_perm=perms)
    for s in tokens:
        m.update(s.encode('utf8'))  
    idx_array = np.array(forest.query(m, num_results))
    if len(idx_array) == 0:
        return None # if your query is empty, return none
    result = database.iloc[idx_array]
    # select columns in the result
    result = result[['title', 'company_name', 'location', 'via', 'description', 
                     'detected_extensions.schedule_type', 'detected_extensions.work_from_home',
                     'detected_extensions.posted_at', 'detected_extensions.salary',
                     'Qualifications', 'Responsibilities', 'Benefits'
                     ]]
    result.columns = ['Job Title', 'Company Name', 'Location', 'Platform', 'Description',
                      'Schedule Type', 'Work from Home', 'Posted at', 'Salary',
                      'Qualifications', 'Responsibilities', 'Benefits']
    
    print('It took %s seconds to query forest.' %(time.time()-start_time))
    return result
# replace nan with empty string
df['Responsibilities'] = df['Responsibilities'].fillna('')
df['Benefits'] = df['Benefits'].fillna('')
df['detected_extensions.schedule_type'] = df['detected_extensions.schedule_type'].fillna('')
df['detected_extensions.work_from_home'] = df['detected_extensions.work_from_home'].fillna('')
df['detected_extensions.posted_at'] = df['detected_extensions.posted_at'].fillna('')
df['detected_extensions.salary'] = df['detected_extensions.salary'].fillna('')
db = df
db['text'] = df['title'] + ' ' + df['company_name'] + ' ' + df['location'] + ' ' + df['description'] + ' ' + df['Qualifications'] + ' ' + df['Responsibilities'] + ' ' + df['Benefits']
forest = get_forest(db, permutations)
# predict results
num_recommendations = 5
# title = 'Data Analyst in DC'
# result = predict(title, db, permutations, num_recommendations, forest)
# print('\n Top Recommendation(s) is(are) \n', result)


import flask
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('Engine.html')

import json
@app.route('/predict', methods=['POST'])
def predict():
    data = json.loads(request.data)
    input_data = str(data['input'])
    prediction = predict(input_data, db, permutations, num_recommendations, forest)
    return str(prediction[0])

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)