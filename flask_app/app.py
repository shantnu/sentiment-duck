#!/usr/bin/env python
from crypt import methods
from flask import Flask, redirect, render_template, \
     request, url_for
import sys
sys.path.append("..")
from dynamodb.update_dynamo import read_dynamodb_data

pos_sent_local = 0
neg_sent_local = 0
app = Flask(__name__)

def update_percents(days):
    global pos_sent_local, neg_sent_local
    positive_counter, negative_counter = read_dynamodb_data(days=days)
    total = positive_counter + negative_counter
    pos_sent_local = int(positive_counter/total * 100)
    neg_sent_local = int(negative_counter/total * 100)

@app.route('/', methods=['GET', 'POST'])
def index():
    global pos_sent_local, neg_sent_local

    return render_template(
        'mvp2.html',
        pos_sent=pos_sent_local, neg_sent=neg_sent_local)

@app.route("/test" , methods=['GET', 'POST'])
def test():
    global pos_sent_local, neg_sent_local
    time_period = request.form.get('comp_select')
    if time_period == "1 day":
        update_percents(1)
    elif time_period == "1 week":
        update_percents(7)
    elif time_period == "1 month":
        update_percents(30)
    else:
        update_percents(365)

    print(f"shan hack time_period = {time_period} pos_sent_local = {pos_sent_local}")
    return redirect(url_for('index'))


if __name__=='__main__':
    app.run(debug=True)
