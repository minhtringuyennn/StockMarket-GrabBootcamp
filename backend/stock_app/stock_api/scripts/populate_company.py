"""
This is a script to populate company table with data fetched from fireant and vndirect api
"""
import requests
import time
from ..models import Company
from ...settings import FIREANT_BEARER_TOKEN
from ..scripts import HTTP_HEADERS

def get_company_list(floor_code):

    VNDIRECT_API_ENDPOINT = f"https://finfo-api.vndirect.com.vn/stocks?floor={floor_code}"

    vndirect_response = requests.get(VNDIRECT_API_ENDPOINT, headers=HTTP_HEADERS)

    company_list = filter(
        lambda company: company['object'] == 'stock', vndirect_response.json()['data'])

    return list(company_list)


def run(*args):
    if args and args[0]:
        market = args[0]
    else:
        market = "HOSE"

    print("BEGIN POPULATING COMPANY TABLE.")

    # Truncating table company
    print("TRUNCATING COMPANY TABLE.")
    Company.objects.all().delete()

    print(f"MARKET TO FETCH: {market}")
    start_time = time.time()
    company_list = get_company_list(market)

    HEADERS = HTTP_HEADERS
    HEADERS['Authorization'] = f"Bearer {FIREANT_BEARER_TOKEN}"
    insert_list = []

    for company in company_list:

        FIREANT_API_ENDPOINT = f"https://restv2.fireant.vn/symbols/{company['symbol']}/fundamental"
        fireant_response = requests.get(
            FIREANT_API_ENDPOINT, headers=HEADERS).json()

        company_info = {
            "symbol": company['symbol'],
            "industry_name": company['industryName'],
            "floor_code": company['floor'],
            "company_name": company['companyName'],
            "shares_outstanding": fireant_response['sharesOutstanding'],
            "dividend_payout_ratio": fireant_response['dividendYield']
        }

        insert_list.append(Company(**company_info))
    
    created_records = Company.objects.bulk_create(insert_list)

    print(f"TOTAL INSERTED RECORDS: {len(created_records)}")
    print(f"TIME ELAPSED: {str(time.time() - start_time)}")
    print("FINISH POPULATING COMPANY TABLE.")
