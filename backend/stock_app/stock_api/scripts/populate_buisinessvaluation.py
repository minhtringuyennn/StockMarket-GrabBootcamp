from contextlib import closing
from django.db import connection
import datetime
from ..models import StockPrice, Company, FinancialStatement, BusinessValuation
import concurrent.futures


financial_statements = FinancialStatement.objects.all()
def zero_division(n, d):
    return n / d if d else -1

def last_date_of_quarter(year, quarter):
    # Return last day of quarter in a year 
    first_quarter_date = datetime.datetime.strptime(str(f'{year if quarter < 4 else year + 1} {(quarter*3 + 1)%12} 01'), '%Y %m %d')
    last_previous_quarter_date = (first_quarter_date - datetime.timedelta(days=1))
    return last_previous_quarter_date.date()
def calBusinessValuation(financial_statement):
    company = financial_statement.company
    symbol = company.symbol
    if (financial_statement.quarter==4):
        near_financial_statements = financial_statements.filter(company_id=symbol,
                                                                year=financial_statement.year, 
                                                                quarter__gte=1,
                                                                quarter__lte=4)
    else:                                                        
        near_financial_statements = financial_statements.filter(company_id=symbol,
                                                                year__gte=(financial_statement.year - 1), 
                                                                year__lte=financial_statement.year).exclude(
                                                                year=financial_statement.year-1,
                                                                quarter__lt=financial_statement.quarter+1).exclude(
                                                                year=financial_statement.year,
                                                                quarter__gt=financial_statement.quarter)
                                                                
    if (len(near_financial_statements)!=4):
#       print(symbol)
#       print(financial_statement.year)
#       print(financial_statement.quarter)
#       print(len(near_financial_statements))
#       print("-------No Financial Statement Enough--------")
        return []
    price_history = StockPrice.objects.filter(company = financial_statement.company, trading_date__date__lte=last_date_of_quarter(financial_statement.year,financial_statement.quarter))
    
    if (len(price_history)>0):
        price_close = price_history.values().latest('trading_date')['price_close']*1000
    else:
#       print(symbol)
#       print(financial_statement.year)
#       print(financial_statement.quarter)
#       print("-------No History Price-------")
        return []

    market_cap = price_close * company.shares_outstanding
    
    book_value = zero_division((financial_statement.total_assets - financial_statement.intangible_assets - financial_statement.liabilities), company.shares_outstanding)
    
    ev = market_cap + financial_statement.shortterm_borrowings_financial_leases + financial_statement.longterm_borrowings_financial_leases - financial_statement.cash_and_cash_equivalents
  
    # 4 quy
    ebit = []
    ebitda = []
    sales4 = []
    eps4 = []
    for near_financial_statement in near_financial_statements:
        ebit.append(near_financial_statement.profit_before_taxes + near_financial_statement.lending_cost)
        ebitda.append(near_financial_statement.profit_before_taxes + near_financial_statement.lending_cost + near_financial_statement.fixed_assets_depreciation)
        sales4.append(near_financial_statement.net_revenue)
        eps4.append(zero_division(near_financial_statement.profit_after_taxes, near_financial_statement.company.shares_outstanding))
    eps = sum(eps4)
    ev_ebit = zero_division(ev, sum(ebit))
    ev_ebitda = zero_division(ev, sum(ebitda))
    
    # 4 quy
    sales = zero_division(ev, sum(sales4))
    
    ev_sales = zero_division(ev, sales)
    
    pb = zero_division(price_close, book_value)
    
    # 4 quy
    pe = zero_division(price_close, eps)
    
    ps = zero_division(market_cap, sales)
    result = [
        symbol,
        financial_statement.year,
        financial_statement.quarter,
        price_close,
        book_value, 
        eps,
        ev,
        ev_ebit,
        ev_ebitda, 
        ev_sales,
        pb,
        pe,
        ps,
        market_cap,
    ]
    return result
# select price_close
# from hercules.stock_api_stockprice 
# where company_id = 'aaa' and trading_date >= timestamp('2022-01-01') 
# order by trading_date asc
# limit 1;

def run(*args):

    print("--BEGIN POPULATING FINANCIAL_RATIO TABLE.--")

    print("TRUNCATING FINANCIAL_RATIO TABLE.")
    with closing(connection.cursor()) as cursor:
        cursor.execute("TRUNCATE TABLE stock_api_businessvaluation")
    businessvaluation_column_list = [field.get_attname_column()[1]
                           for field in BusinessValuation._meta.fields[1:]]
    sql = f"INSERT INTO stock_api_businessvaluation ({','.join(businessvaluation_column_list)}) VALUES "
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
        # Start the load operations and mark each future with its URL
        future_to_bv = {executor.submit(calBusinessValuation, financial_statement): financial_statement for financial_statement in financial_statements}
        for future in concurrent.futures.as_completed(future_to_bv):
            symbol = future_to_bv[future].company.symbol
            result = future.result()
            if (result != []):
                temp_sql = sql + ', '.join(['(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'])
                cursor = connection.cursor()
                try:
                    cursor.execute(temp_sql, result)
                except Exception as e:
                    print(f"Exception: {str(e)}")
                cursor.close()
                print(symbol + " success")
    print("FINISH POPULATING FINANCIAL_RATIO TABLE.")
