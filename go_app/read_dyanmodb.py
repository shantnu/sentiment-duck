#!../env/bin/python
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute,UTCDateTimeAttribute,NumberAttribute
import datetime
from datetime import timedelta
import sys
from json import dump
import os
class SentiModel(Model):
    """
    A DynamoDB User
    """
    class Meta:
        table_name = "sentiment-duck-data"
        region = "us-east-1"
    date_data = UTCDateTimeAttribute(hash_key=True)
    sentiment_positive = NumberAttribute(default=0)
    sentiment_negative = NumberAttribute(default=0)
    stock_change_percent = NumberAttribute(default=0.0)

def read_dynamodb_data(days):
    if os.path.exists("dynamodata.json"):
        os.remove("dynamodata.json")
    date_filter = datetime.date.today() - timedelta(days = days)
    print("shantnu debug date_filter=",date_filter)

    counter = 0
    positive_counter = 0
    negative_counter = 0
    stock_counter = 0.0
    for item in SentiModel.scan():
        counter += 1
        print("Item queried from index: {0}".format(item))
        positive_counter += item.sentiment_positive
        negative_counter += item.sentiment_negative
        stock_counter += item.stock_change_percent
        if item.date_data.date() < date_filter:
            break
    print("before : ",positive_counter, negative_counter,stock_counter , counter)
    positive_counter = positive_counter / counter
    negative_counter = negative_counter / counter
    stock_counter = stock_counter / counter #yeah, not perfect but im lazy :/
    stock_counter = float("{:.2f}".format(stock_counter))
    print("after : ",positive_counter, negative_counter, stock_counter, counter)

    output = {
        "positive_counter":positive_counter,
        "negative_counter": negative_counter,
        "stock_counter":stock_counter

    }


    with open("dynamodata.json", 'w') as file:
	    dump(output, file)
    return positive_counter, negative_counter, stock_counter
if __name__ == "__main__":
    days = int(sys.argv[1])
    print("datye=", days)
    #update_dynamodb(datetime.datetime.now(), 22,55,-7.5 )
    positive_counter, negative_counter, stock_counter = read_dynamodb_data(days)
    total = positive_counter + negative_counter
    pos_percent = int(positive_counter/total * 100)
    neg_percent = int(negative_counter/total * 100)

    print("Dynamo values #", pos_percent,neg_percent, stock_counter, "#")
