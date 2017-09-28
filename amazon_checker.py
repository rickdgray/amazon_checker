# some test asins:
# metroid prime 4 B072JYMLT3
# metroid 2 remake B071X7V8NR
# mario odd B01MY7GHKJ
# snes classic B0721GGGS9

import sys
import time
from datetime import datetime
import decimal
from amazon.api import AmazonAPI
from amazon.api import AsinNotFound
from amazon.api import RequestThrottled
from urllib import error
from tabulate import tabulate
import boto3

# in each tuple: Name as string, ASIN as string, WANTED price (for waiting on a sale) as decimal
# items_to_parse = [['Metroid Prime 4', 'B072JYMLT3', decimal.Decimal(100.00)], \
#                   ['Metroid 2', 'B071X7V8NR', decimal.Decimal(100.00)], \
#                   ['Mario Odyssey', 'B01MY7GHKJ', decimal.Decimal(100.00)]]
items_to_parse = [['Super NES Classic', 'B0721GGGS9', decimal.Decimal(79.99)]]
# how often to call amazon api in seconds; no less than 1 for sure
poll_rate = 2

SNS = boto3.client('sns')
PHONE_NUMBER = '+15555555555'
ACCESS_KEY_ID = 'XXXXXXXXXXXXXXXXXXXX'
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
ASSOC_TAG = 'somethingorother05-20'


def alert_of_uncaught_exception(exctype, value, tb):
    SNS.publish(PhoneNumber=PHONE_NUMBER, Message='shit went bad: check amazon checker')
    print('Type: ', exctype)
    print('Value: ', value)
    print('Traceback: ', tb)


sys.excepthook = alert_of_uncaught_exception


def build_table(item):
    item_info = []
    item_info.append(['ASIN', item.asin])
    item_info.append(['Availability', item.availability])
    item_info.append(['Formatted Price', item.formatted_price])
    item_info.append(['Is Preorder', item.is_preorder])
    item_info.append(['List Price', item.list_price])
    item_info.append(['Price', item.price_and_currency[0]])
    item_info.append(['Currency', item.price_and_currency[1]])
    item_info.append(['Release Date', item.release_date])
    item_info.append(['SKU', item.sku])
    item_info.append(['UPC', item.upc])
    item_info.append(['Title', item.title])

    return item_info


if __name__ == '__main__':
    amazon = AmazonAPI(ACCESS_KEY_ID, SECRET_KEY, ASSOC_TAG)

    sales = []
    success = 0
    total = 0

    while True:
        for each in items_to_parse:
            try:
                total = total + 1
                item = amazon.lookup(ItemId=each[1], ResponseGroup='OfferFull', IncludeReviewsSummary=False)

                success = success + 1
                print('[' + datetime.now().strftime('%b %d %H:%M') +
                      '] Success Rate: ' + str(success) + '/' + str(total) +
                      '({0:.2f}%)'.format((success / total) * 100) +
                      ' Result: Item found!')

                # if item is found print out a table (for debug)
                item_info = build_table(item)
                print(each[0])
                print(tabulate(item_info, headers=['Content', 'Value'], tablefmt='pipe'))

                if item.price_and_currency[0] <= each[2]:
                    print('And is on sale!')
                    sales.append([each[0], item.price_and_currency[0]])
                else:
                    print('But was not on sale...')

            except AsinNotFound:
                success = success + 1
                print('[' + datetime.now().strftime('%b %d %H:%M') +
                      '] Success Rate: ' + str(success) + '/' + str(total) +
                      '({0:.2f}%)'.format((success / total) * 100) +
                      ' Result: ASIN not found (this is normal)')

            except RequestThrottled:
                print('[' + datetime.now().strftime('%b %d %H:%M') +
                      '] Success Rate: ' + str(success) + '/' + str(total) +
                      '({0:.2f}%)'.format((success / total) * 100) +
                      ' Result: API call was throttled')

            except error.HTTPError:
                print('[' + datetime.now().strftime('%b %d %H:%M') +
                      '] Success Rate: ' + str(success) + '/' + str(total) +
                      '({0:.2f}%)'.format((success / total) * 100) +
                      ' Result: 503 Service Unavailable')

            if not sales:
                pass

            else:
                # Huzzah! an item is on sale! alert the boss!
                message = 'On Sale!\n'
                for each_ in sales:
                    message = message + each_[0] + ': ' + str(each_[1]) + '\n'
                SNS.publish(PhoneNumber=PHONE_NUMBER, Message=message)

            time.sleep(poll_rate)
