#!/usr/bin/env python
from crypt import methods
from flask import Flask, flash, redirect, render_template, \
     request, url_for

pos_sent_local = 0
neg_sent_local = 0
app = Flask(__name__)

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
        pos_sent_local = 33
        neg_sent_local = 99
    elif time_period == "1 week":
        pos_sent_local = 330
        neg_sent_local = 990
    else:
        pos_sent_local = 76
        neg_sent_local = 24
    print(f"shan hack time_period = {time_period} pos_sent_local = {pos_sent_local}")
    return redirect(url_for('index'))


if __name__=='__main__':
    app.run(debug=True)
