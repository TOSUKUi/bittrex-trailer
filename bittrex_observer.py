import requests
from influxdb import InfluxDBClient
from slack_utils import SlackUtils
import time
import sys
import traceback
import logging

def main():
    print("START^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    logging.info("unko")
    execute()


def execute():
    slack = SlackUtils()
    client = connect_influxdb()
    while True:
        try:
            summary = get_markets_summaries()
            if summary["success"]:
                data = map(data_format, summary["result"])
                client.write_points(data)
            else:
                slack.warn(message="message={message}".format(message=summary["message"]), channel="bittrex")
            time.sleep(60)
        except:
            error = traceback.format_exc()
            slack.danger(message=error, channel="bittrex")
            print(error)
            exit(1)


def connect_influxdb():
    client = InfluxDBClient(host='localhost', port=8086, username='root', password='root', database='bittrex')
    dbs = client.get_list_database()
    bittrex_db = {'name': 'bittrex'}
    if bittrex_db not in dbs:
        client.create_database('bittrex')
    return client


def get_markets_summaries():
    url = 'https://bittrex.com/api/v1.1/public/getmarketsummaries'
    response = requests.get(url)
    if response.status_code % 200 < 100:
        return response.json()


def data_format(summary_result):
    data = {
        'fields': fields_format(summary_result),
        'tags': tags_format(summary_result),
        'measurement': 'markets'
    }
    print (data)
    return data


def fields_format(summary):
    return {
        '24h_high': summary["High"],
        '24h_low': summary["Low"],
        'volume': summary["Volume"],
        'bid': summary["Bid"],
        'ask': summary["Ask"],
        'last': summary["Last"],
        'open_buy_orders': summary["OpenBuyOrders"],
        'open_sell_orders': summary["OpenSellOrders"],
    }


def tags_format(summary):
    return {
        'base_coin': summary["MarketName"].split('-')[0],
        'another_coin': summary["MarketName"].split('-')[1]
    }


if __name__=="__main__":
    main()
