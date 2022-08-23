from datetime import datetime
from stock_app.stock_api.scripts.populate_stockprice import populate_stockprice
from stock_app.stock_api.scripts.populate_marketprice import populate_marketprice


def update_stock_price():
    """
    Update stock price within 5 minutes
    """
    print(f"{str(datetime.today())} :")
    populate_stockprice(
        start_date=datetime.today().strftime('%Y-%m-%d'), verbose=True, upsert=True)


def update_market_price():
    """
    Update stock price within 5 minutes
    """
    print(f"{str(datetime.today())} :")
    populate_marketprice( verbose=True, upsert=True )
