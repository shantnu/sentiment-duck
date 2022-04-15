from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute,UTCDateTimeAttribute,NumberAttribute
import datetime

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

def read_dynamodb_data():

    for item in SentiModel.scan():
        print("Item queried from index: {0}".format(item))
if __name__ == "__main__":
    #update_dynamodb(datetime.datetime.now(), 22,55,-7.5 )
    read_dynamodb_data()
