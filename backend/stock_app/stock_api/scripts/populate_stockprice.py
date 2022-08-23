"""
This file contains functions to populate & update 
stockprice table with data fetched from fireant api
"""
from contextlib import closing
from datetime import timezone
import time
import requests
from ..models import StockPrice, Company
from django.db import connection
from ...settings import FIREANT_BEARER_TOKEN
from ..scripts import HTTP_HEADERS
from datetime import datetime
import concurrent.futures

END_DATE = datetime.today().strftime('%Y-%m-%d')
MAX_LIMIT = 10000
OFFSET = 0

def updatePrice(symbol, start_date):
    api_endpoint = f"https://restv2.fireant.vn/symbols/{symbol}/historical-quotes"

    params = {
        "startDate": start_date,
        "endDate": END_DATE,
        "offset": OFFSET,
        "limit": MAX_LIMIT
    }
    HEADERS = HTTP_HEADERS
    HEADERS['Authorization'] = f'Bearer {FIREANT_BEARER_TOKEN}'
    api_response = requests.get(
        api_endpoint, headers=HEADERS, params=params).json()
    return api_response
    
def populate_stockprice(start_date, upsert=False, verbose=False):

    company_list = Company.objects.all()


    stock_price_column_list = [field.get_attname_column()[1]
                               for field in StockPrice._meta.fields[1:]]

    cursor = connection.cursor()

    sql = f"INSERT INTO stock_api_stockprice ({','.join(stock_price_column_list)}) VALUES "

    start_time = time.time()

    row_cnt = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
        # Start the load operations and mark each future with its URL
        future_to_stock = {executor.submit(updatePrice, company.symbol, start_date): company for company in company_list}
        for future in concurrent.futures.as_completed(future_to_stock):
            symbol = future_to_stock[future].symbol
            stock_history_price = []
            api_response = future.result()
            for trade in api_response:
                stock_history_price.extend([
                    symbol,
                    datetime.fromisoformat(trade["date"]),
                    trade["priceHigh"],
                    trade["priceLow"],
                    trade["priceOpen"],
                    trade["priceClose"],
                    trade["totalVolume"],
                    trade["totalValue"],
                    trade["buyForeignValue"],
                    trade["sellForeignValue"]
                ])
            temp_sql = sql + ', '.join(['(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)']
                                       * len(api_response))

            if upsert:
                temp_sql += "AS new ON DUPLICATE KEY UPDATE {}".format(
                    ', '.join([f"{column} = new.{column}"for column in stock_price_column_list]))

            # Batch insert all stock_price records of a company
            try:
                cursor.execute(temp_sql, stock_history_price)
                row_cnt += cursor.rowcount
            except Exception as e:
                print(f"Exception: {str(e)}")
    
    if verbose:
        if upsert:
            print(f"TOTAL UPSERTED RECORDS: {row_cnt}")
        else:
            print(f"TOTAL INSERTED RECORDS: {row_cnt}")
        print(f"TIME ELAPSED: {str(time.time() - start_time)}")
        print("--FINISH INSERTING STOCK_PRICE TABLE--")
    
    cursor.close()


def run(*args):
    if args and args[0]:
        start_date = args[0]
    else:
        start_date = "2015-01-01"

    print("--BEGIN POPULATING STOCK_PRICE TABLE.--")

    print("TRUNCATING STOCK_PRICE TABLE.")
    with closing(connection.cursor()) as cursor:
        cursor.execute("TRUNCATE TABLE stock_api_stockprice")

    # Get historical trades within input interval for each company
    populate_stockprice(start_date=start_date, verbose=True)
