import re
import bert
import nltk
from scipy import spatial
import numpy as np
import pandas as pd
from flask import Flask
from flask import Flask, render_template, request
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)

vectors, sentences = bert.vectorizer()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    statement = request.args.get('msg')
    # print(bert.s_bert(statement))
    a = []
    for i in range(len(vectors)):
        print( 1 - spatial.distance.cosine(vectors[i], bert.s_bert(statement)))
        a.append( 1 - spatial.distance.cosine(vectors[i], bert.s_bert(statement)))
    
    max_value = max(a)
    max_index = a.index(max_value)

    return sentences[max_index]

if __name__ == '__main__':
   app.run(debug = True)
