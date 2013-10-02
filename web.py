#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import twitter
import operator
import os
import re

from flask import Flask, request, render_template

api = twitter.Api(
    consumer_key        = os.getenv('CONSUMER_KEY'),
    consumer_secret     = os.getenv('CONSUMER_SECRET'),
    access_token_key    = os.getenv('ACCESS_TOKEN_KEY'),
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET'),
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    twitterScreenNames = [screenName[1:] if screenName.startswith('@') else screenName for screenName in re.split(' |,', request.form['twitterScreenNames'])]

    # collect documents
    documents = {}
    for twitterScreenName in twitterScreenNames:
        statuses = api.GetUserTimeline(screen_name = twitterScreenName, count = 100)
        documents[twitterScreenName] = ' '.join([s.text.lower() for s in statuses])

    (tfIdf, allWords) = calcTfIdf(documents)

    return render_template('result.html', var = {
        'twitterScreenNames': twitterScreenNames,
        'tfIdf': tfIdf,
        'allWords': list(allWords)
    })

def calcTfIdf(documents):
    tfIdf = {user: {} for user in documents.keys()}

    allWords = set()
    N = len(documents)
    for user in documents:
        words = re.split(' |,|\.|:|;|"|\*|!|\?|\{|\}|\(|\)|\[|\]', documents[user])

        # calc tf
        tf = {}
        for word in words:
            if word == '': continue
            if len(word) < 4: continue
            tf[word] = tf[word] + 1 if (word in tf) else  1

        # calc df (@TODO: no need to calculate df everytime)
        df = {k: 0 for k in tf.keys()}
        for word in tf.keys():
            df[word] = sum([1 for k in documents if (-1 < documents[k].find(word))])

        # calc tf-idf
        for word in tf.keys():
            score = tf[word] * math.log(float(N) / float(df[word]))
            if 0 < score: tfIdf[user][word] = score

        # modify words which should be calculated
        for word in tf.keys():
            if word in tfIdf[user]: allWords.add(word)

    # sort
    for user in tfIdf.keys():
        tfIdf[user] = sorted(tfIdf[user].iteritems(), key = operator.itemgetter(1), reverse = True)

    return (tfIdf, allWords)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0',
            port=port,
            debug=True,
            )
