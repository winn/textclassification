#!/usr/bin/python
#-*-coding: utf-8 -*-
##from __future__ import absolute_import
######

import pickle
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)
api = Api(app)

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


api.add_resource(get_classify, '/classify',endpoint='classify')

if __name__ == '__main__':
    app.run(threaded=True)