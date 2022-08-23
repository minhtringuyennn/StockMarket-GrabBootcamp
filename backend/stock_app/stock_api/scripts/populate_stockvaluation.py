"""
This file contains functions to populate & update 
stockprice table with data fetched from fireant api
"""
from contextlib import closing
from datetime import timezone
import time
import requests
from ..models import Company, BusinessValuation, StockValuation
from django.db import connection
from datetime import datetime
import concurrent.futures

END_DATE = datetime.today().strftime('%Y-%m-%d')
MAX_LIMIT = 10000
OFFSET = 0

def zero_division(n, d):
    return n / d if d else -1

def calculate_upsize(a, b):
    if b == 0:
        return -1
    if b == -1:
        return -1
    return (a - b) / b * 100


def updateValuation(symbol, year, quarter):
    column_list = [field.get_attname_column()[1]
                            for field in BusinessValuation._meta.fields[1:]]
    Val_List = {}
    for column in column_list:
        Val_List.update({column : []})
    company = Company.objects.get(symbol=symbol)
    Val_List.update({'industry_name': company.industry_name})
    
    ref_valuation = BusinessValuation.objects.get(company=symbol, year=year, quarter=quarter)
    same_industry_list = Company.objects.filter(industry_name=company.industry_name).values_list('symbol', flat=True)
    for stock in same_industry_list:
        try:
            valuation = BusinessValuation.objects.get(company=stock, year=year, quarter=quarter)
            for column in column_list:
                Val_List[column].append(getattr(valuation, column))
        except BusinessValuation.DoesNotExist:
            continue
    result = [
        str(symbol),
        str(max(Val_List['book_value'])),
        str(min(Val_List['book_value'])),
        str(zero_division(sum(Val_List['book_value']),len(Val_List['book_value']))),
        str(calculate_upsize(ref_valuation.book_value, zero_division(sum(Val_List['book_value']),len(Val_List['book_value'])))),
        
        str(max(Val_List['earnings_per_share'])),
        str(min(Val_List['earnings_per_share'])),
        str(zero_division(sum(Val_List['earnings_per_share']),len(Val_List['earnings_per_share']))),
        str(zero_division(ref_valuation.earnings_per_share , zero_division(sum(Val_List['earnings_per_share']),len(Val_List['earnings_per_share'])))),
        
        str(max(Val_List['enterprise_value'])),
        str(min(Val_List['enterprise_value'])),
        str(zero_division(sum(Val_List['enterprise_value']),len(Val_List['enterprise_value']))),
        str(calculate_upsize(ref_valuation.enterprise_value, zero_division(sum(Val_List['enterprise_value']),len(Val_List['enterprise_value'])))),
        
        str(max(Val_List['ev_over_ebit'])),
        str(min(Val_List['ev_over_ebit'])),
        str(zero_division(sum(Val_List['ev_over_ebit']),len(Val_List['ev_over_ebit']))),
        str(calculate_upsize(ref_valuation.ev_over_ebit, zero_division(sum(Val_List['ev_over_ebit']),len(Val_List['ev_over_ebit'])))),
        
        str(max(Val_List['ev_over_ebitda'])),
        str(min(Val_List['ev_over_ebitda'])),
        str(zero_division(sum(Val_List['ev_over_ebitda']),len(Val_List['ev_over_ebitda']))),
        str(calculate_upsize(ref_valuation.ev_over_ebitda, zero_division(sum(Val_List['ev_over_ebitda']),len(Val_List['ev_over_ebitda'])))),
        
        str(max(Val_List['ev_sales'])),
        str(min(Val_List['ev_sales'])),
        str(zero_division(sum(Val_List['ev_sales']),len(Val_List['ev_sales']))),
        str(calculate_upsize(ref_valuation.ev_sales, zero_division(sum(Val_List['ev_sales']),len(Val_List['ev_sales'])))),
        
        str(max(Val_List['price_to_book'])),
        str(min(Val_List['price_to_book'])),
        str(zero_division(sum(Val_List['price_to_book']),len(Val_List['price_to_book']))),
        str(calculate_upsize(ref_valuation.price_to_book, zero_division(sum(Val_List['price_to_book']),len(Val_List['price_to_book'])))),
        
        str(max(Val_List['price_earnings'])),
        str(min(Val_List['price_earnings'])),
        str(zero_division(sum(Val_List['price_earnings']),len(Val_List['price_earnings']))),
        str(calculate_upsize(ref_valuation.price_earnings, zero_division(sum(Val_List['price_earnings']),len(Val_List['price_earnings'])))),
        
        str(max(Val_List['price_to_sales'])),
        str(min(Val_List['price_to_sales'])),
        str(zero_division(sum(Val_List['price_to_sales']),len(Val_List['price_to_sales']))),
        str(calculate_upsize(ref_valuation.price_to_sales,zero_division(sum(Val_List['price_to_sales']),len(Val_List['price_to_sales'])))),
        
        str(max(Val_List['market_cap'])),
        str(min(Val_List['market_cap'])),
        str(zero_division(sum(Val_List['market_cap']),len(Val_List['market_cap']))),
        str(calculate_upsize(ref_valuation.market_cap, zero_division(sum(Val_List['market_cap']),len(Val_List['market_cap']))))
    ]
    return result
    
def populate_stockvaluation(year, quarter, upsert=False, verbose=False):

    company_list = Company.objects.all()


    STOCK_VALUATION_column_list = [field.get_attname_column()[1]
                               for field in StockValuation._meta.fields[1:]]

    cursor = connection.cursor()

    sql = f"INSERT INTO stock_api_stockvaluation ({','.join(STOCK_VALUATION_column_list)}) VALUES "

    start_time = time.time()

    row_cnt = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
        # Start the load operations and mark each future with its URL
        future_to_stock = {executor.submit(updateValuation, company.symbol, year, quarter): company for company in company_list}
        for future in concurrent.futures.as_completed(future_to_stock):
            symbol = future_to_stock[future].symbol
            result = future.result()
            temp_sql = sql + ', '.join(['(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'])
            if upsert:
                temp_sql += "AS new ON DUPLICATE KEY UPDATE {}".format(
                    ', '.join([f"{column} = new.{column}"for column in STOCK_VALUATION_column_list]))

            # Batch insert all STOCK_VALUATION records of a company
            try:
                cursor.execute(temp_sql, result)
                row_cnt += cursor.rowcount
                print(f"{symbol} successfully inserted")
            except Exception as e:
                print(f"Exception: {str(e)}")
    
    if verbose:
        if upsert:
            print(f"TOTAL UPSERTED RECORDS: {row_cnt}")
        else:
            print(f"TOTAL INSERTED RECORDS: {row_cnt}")
        print(f"TIME ELAPSED: {str(time.time() - start_time)}")
        print("--FINISH INSERTING STOCK_VALUATION TABLE--")
    
    cursor.close()


def run(*args):
    print("--BEGIN POPULATING STOCK_VALUATION TABLE.--")

    print("TRUNCATING STOCK_VALUATION TABLE.")
    with closing(connection.cursor()) as cursor:
        cursor.execute("TRUNCATE TABLE stock_api_stockvaluation")

    # Get historical trades within input interval for each company
    populate_stockvaluation(year=2022, quarter=1, verbose=True)
