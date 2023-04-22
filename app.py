#!/usr/bin/python
#-*-coding: utf-8 -*-
##from __future__ import absolute_import
######

import pickle
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

app = Flask(__name__)
api = Api(app)

url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRdDyIzjzb8uyiCEqkoBQlPychRQw64jUDruw64gbvlYzzoauGCljvhNNrRl-hqhx_uGER6FJDu0C4X/pub?gid=1104547283&single=true&output=csv'
dat = pd.read_csv(url)

@app.route('/')
def index():
    return "Hello World!"
# Load the pipeline model from the pickle file
with open('model.pkl', 'rb') as f:
    pipeline = pickle.load(f)

# Define the route for the API
class get_classify(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('text', type=str)
        dictp = parser.parse_args()
        text = dictp['text']
        print(text)
        res = pipeline.predict([text])[0]
        return res

def randrow(topic=None):
    if topic!=None:
        topic = topic.lower()
        #return dat
        sdat = dat[(dat.iloc[:,3].str.find('Health')!=-1) & (dat.iloc[:,3].notnull())]
        res = sdat.sample(1).iloc[0].values
    else:
        res = dat.sample(1).iloc[0].values
    topic = res[3]
    prob = res[8]
    sol = res[9]
    out = {}
    out['topic'] = topic
    out['problem'] = prob
    out['solution'] = sol
    return out

class get_data(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('topic', type=str)
        dictp = parser.parse_args()
        topic = dictp['topic']
        out = randrow(topic)

        return out




api.add_resource(get_data, '/data',endpoint='data')
api.add_resource(get_classify, '/classify',endpoint='classify')

if __name__ == '__main__':
    app.run(threaded=True)