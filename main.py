from get_senti.finance import get_finance_data
from get_senti.get_reddit import get_redit_data
from dynamodb.update_dynamo import update_dynamodb
import requests

import datetime

final_pos, final_neg = get_redit_data()
stock_percent = get_finance_data()

print("\n --------------")
print(final_pos, final_neg, stock_percent)
print("\n -------------- Updating dynamo \n")
update_dynamodb(date_obj=datetime.datetime.now(), final_pos=final_pos, final_neg=final_neg, stock_percent=stock_percent)
requests.get("https://hc-ping.com/f1c6213b-14fb-46fd-87f4-a83a7dbf2980")