import requests
from influxdb import InfluxDBClient
from slack_utils import SlackUtils
import time
from datetime import datetime
import traceback
import logging


def main():
    execute()


def logger_builder(name):
    """
    return logger
    :param name: log file name
    :return: logger
    """
    logging.basicConfig(format="[%(asctime)s] %(levelname)s - %(message)s", filemode='a',
                        filename="log/{date}-{name}.log".format(date=datetime.now().strftime("%Y-%m-%d"),
                                                                name=name), level=logging.INFO)
    return logging.getLogger()


def execute():
    logger = logger_builder("exec")
    logger.info("start")
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
            logger.error(error)
            slack.danger(message=error, channel="bittrex")
            exit(1)


def connect_influxdb():
    logger_builder("exec").info("connect influxdb...")
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
