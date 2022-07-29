import json
import boto3
import requests
from bs4 import BeautifulSoup
import re
import datetime


def lambda_handler(event, context):
    ses = boto3.client("ses")
    sns = boto3.client('sns')
    source = "http://sentimentduck.com"

    r = requests.get(source)
    # body = {
    #     "message": r,
    #     "input": event,
    # }

    soup = BeautifulSoup(r.text)

    # print(soup)

    full_text = ""

    for pp in soup.body.find_all("p"):
        full_text += pp.text
    line = full_text.split("\r\n")[0]
    pos = re.findall("([\d]*) % positive", line)[0]
    neg = re.findall("([\d]*)% Neg", line)[0]
    stock = re.findall("😠 [\w]* ([+-.\d]*)", line)[0]

    print(pos, neg, stock)

    datenow=datetime.datetime.now().date().strftime("%B-%d-%Y")
    email_data =  f" Sentiment data: \n Positive= {pos}\n Negative = {neg} \n stock = {stock}\n"
    subject ="Sentiment data update: " + datenow
    print(email_data)

    ses.send_email(
        Source="shantnu@shantnutiwari.com",
        Destination={"ToAddresses": ["shantnu@shantnutiwari.com"]},
        Message={
            "Subject": {"Data": subject},
            "Body": {"Text":  {'Data': email_data}},
        },
    )
    day =  datetime.datetime.now().weekday()

    if day == 6: #only on Sundays
        number = '+447792766186'
        sns.publish(PhoneNumber = number, Message=email_data)
    return True


if __name__ == "__main__":
    hello("d", "")

