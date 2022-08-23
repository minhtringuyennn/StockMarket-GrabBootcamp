"""
This is a script to populate marketprice table with data
fetched from wichart api
"""
from contextlib import closing
from datetime import timezone, datetime
import time
import requests
from ..models import MarketPrice
from ..scripts import HTTP_HEADERS
from datetime import datetime
from django.db import connection


def populate_marketprice(verbose=False, upsert=False):
    api_endpoint = f"https://wichart.vn/wichartapi/wichart/chartthitruong"

    HEADERS = HTTP_HEADERS

    market_list = [
        {'VNINDEX':    'VN-INDEX'},
        {'HNX':        'HNX-INDEX'},
        {'dji':        'DOW JONES'},
        {'gdaxi':      'DAX'},
        {'ftse':       'FTSE 100'},
        {'n225':       'Nikkei 225'},
        {'ks11':       'KOSPI'},
        {'ssec':       'Shanghai'}
    ]
  
    start_time = time.time()

    market_price_column_list = [field.get_attname_column()[1]
                                for field in MarketPrice._meta.fields[1:]]

    cursor = connection.cursor()
    row_cnt = 0
    sql = f"INSERT INTO stock_api_marketprice ({','.join(market_price_column_list)}) VALUES "

    for market in market_list:

        short_name, market_symbol = market.popitem()
        params = {"code": short_name}
        market_history_price = []

        api_response = requests.get(
            api_endpoint, headers=HEADERS, params=params).json()

        for trading_date, price_close in api_response['listClose']:
            if price_close == None:
                continue
            market_history_price.extend(
                [market_symbol.upper(),
                 datetime.fromtimestamp(
                     trading_date/1000),
                 price_close]
            )
        
        if upsert:
            temp_sql = sql + '(%s, %s, %s) ' + 'AS new ON DUPLICATE KEY UPDATE {}'.format(
                ', '.join([f"{column} = new.{column}"for column in market_price_column_list]))
        else:
            temp_sql = sql + ', '.join(['(%s, %s, %s)']
                                   * (len(market_history_price) // 3) )

        # Batch insert or upsert all market_price records of an index
        try:
            if upsert:
                cursor.execute(temp_sql, market_history_price[:3])
            else:
                cursor.execute(temp_sql, market_history_price)
            row_cnt += cursor.rowcount
        except Exception as e:
            print(f"Exception: {str(e)}")

    if verbose:
        if upsert:
            print(f"TOTAL UPSERTED RECORDS: {row_cnt}")
        else:
            print(f"TOTAL INSERTED RECORDS: {row_cnt}")
        print(f"TIME ELAPSED: {str(time.time() - start_time)}")
        print("--FINISH POPULATING MARKET_PRICE TABLE--")

    cursor.close()


def run(*args):

    print("--BEGIN POPULATING MARKET_PRICE TABLE.--")

    print("TRUNCATING MARKET_PRICE TABLE.")
    with closing(connection.cursor()) as cursor:
        cursor.execute("TRUNCATE TABLE stock_api_marketprice")

    # Get historical trades of common index around the world
    populate_marketprice(verbose=True)
