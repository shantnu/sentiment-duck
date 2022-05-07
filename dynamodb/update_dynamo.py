from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute,UTCDateTimeAttribute,NumberAttribute
import datetime
from datetime import timedelta
import sys

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

def create_table():
    SentiModel.create_table(read_capacity_units=1, write_capacity_units=1)

def update_dynamodb(date_obj, final_pos, final_neg, stock_percent):
    user = SentiModel(date_data = date_obj, sentiment_positive = final_pos, sentiment_negative = final_neg, stock_change_percent = stock_percent)
    user.save()

def read_dynamodb_data(days):
    date_filter = datetime.date.today() - timedelta(days = days)
    print("shantnu debug date_filter=",date_filter)

    counter = 0
    positive_counter = 0
    negative_counter = 0
    for item in SentiModel.scan():
        counter += 1
        print("Item queried from index: {0}".format(item))
        print("read item = ", item.sentiment_positive, item.sentiment_negative)
        positive_counter += item.sentiment_positive
        negative_counter += item.sentiment_negative
        if item.date_data.date() < date_filter:
            break
    print("before : ",positive_counter, negative_counter,counter)
    positive_counter = positive_counter / counter
    negative_counter = negative_counter / counter
    print("after : ",positive_counter, negative_counter,counter)
    return positive_counter, negative_counter
if __name__ == "__main__":
    #update_dynamodb(datetime.datetime.now(), 22,55,-7.5 )
    positive_counter, negative_counter = read_dynamodb_data(int(sys.argv[1]))
    total = positive_counter + negative_counter
    pos_percent = int(positive_counter/total * 100)
    neg_percent = int(negative_counter/total * 100)

    print("percnts = ", pos_percent,neg_percent)
