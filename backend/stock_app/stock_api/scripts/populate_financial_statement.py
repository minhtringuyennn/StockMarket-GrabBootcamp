"""

"""
from contextlib import closing
from datetime import timezone
import time
from ..models import StockPrice, Company, FinancialStatement
from django.db import connection
from ...settings import FIREANT_BEARER_TOKEN
from ..scripts import HTTP_HEADERS
from datetime import datetime
import requests, json, re
import concurrent.futures



def cleanRoman(text):
    pattern = r'\b(?=[MDCLXVIΙ])M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})([IΙ]X|[IΙ]V|V?[IΙ]{0,3})\b\.?'
    return re.sub(pattern, '', text)

def cleanText(text):
    pattern = r'[^A-Za-z]+'
    return re.sub(pattern, '', text)

def cleanBullet(text):
    pattern = '\w[.)]\s*'
    return re.sub(pattern, '', text)

def removeVietNameAccent(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s

def removeSpace(text):
    pattern = r'\s*'
    return re.sub(pattern, '', text)


def updateCompany(symbol = "TCB", fromYear = 2019, toYear = 2019):
    """
    """
    companyInfo = []
    HEADERS                 = {'content-type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla'}
    FIREANT_BEARER_TOKEN    = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSIsImtpZCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4iLCJhdWQiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4vcmVzb3VyY2VzIiwiZXhwIjoxOTM5NDc0NDY3LCJuYmYiOjE2Mzk0NzQ0NjcsImNsaWVudF9pZCI6ImZpcmVhbnQudHJhZGVzdGF0aW9uIiwic2NvcGUiOlsib3BlbmlkIiwicHJvZmlsZSIsInJvbGVzIiwiZW1haWwiLCJhY2NvdW50cy1yZWFkIiwiYWNjb3VudHMtd3JpdGUiLCJvcmRlcnMtcmVhZCIsIm9yZGVycy13cml0ZSIsImNvbXBhbmllcy1yZWFkIiwiaW5kaXZpZHVhbHMtcmVhZCIsImZpbmFuY2UtcmVhZCIsInBvc3RzLXdyaXRlIiwicG9zdHMtcmVhZCIsInN5bWJvbHMtcmVhZCIsInVzZXItZGF0YS1yZWFkIiwidXNlci1kYXRhLXdyaXRlIiwidXNlcnMtcmVhZCIsInNlYXJjaCIsImFjYWRlbXktcmVhZCIsImFjYWRlbXktd3JpdGUiLCJibG9nLXJlYWQiLCJpbnZlc3RvcGVkaWEtcmVhZCJdLCJzdWIiOiJkM2UxY2I4MC0xMDc0LTRhMjItYWY4Ny0yNjlhOGM3Mzc2NmMiLCJhdXRoX3RpbWUiOjE2Mzk0NzQ0NjcsImlkcCI6Ikdvb2dsZSIsIm5hbWUiOiJtaW5odHJpLm1pbmh6enh6eEBnbWFpbC5jb20iLCJzZWN1cml0eV9zdGFtcCI6ImIzNDM3MmFkLTgxZjktNGUyYy04NTc4LTBmYWE3NmIxYmMzOSIsInByZWZlcnJlZF91c2VybmFtZSI6Im1pbmh0cmkubWluaHp6eHp4QGdtYWlsLmNvbSIsInVzZXJuYW1lIjoibWluaHRyaS5taW5oenp4enhAZ21haWwuY29tIiwiZnVsbF9uYW1lIjoiTWluaCBUcmkgTmd1eWVuIiwiZW1haWwiOiJtaW5odHJpLm1pbmh6enh6eEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6InRydWUiLCJqdGkiOiIzY2FjMTQwZGIxMTRkNGMwOWI2MWJjNTA1NmQ0MDg0OCIsImFtciI6WyJleHRlcm5hbCJdfQ.X9deVcDttd06BxdZC7uOBXeObi3qOYqIsWK190UXRBSbVw-03W4KlsQ5PwKyoAc5beog9zYTtZzoE63cnbJ4o14aq4ljsM4bcFEfP2wLl3taVjuKbJOKaFMLiUFyQGiPc5_iE7b-7Z3cVWyEWtDl9xeqg57vVrBLXvcyzquWTFVKgaumR7PA3EwM5UHQWL8f2nx_zwAW06Y-x6soQItu8byN4Brm6VZK6YawUikZqsNehRxHmd_Q52rd4WJ5cTnLUHSlHNoKzEVOobfvOStE2bkoEceBuwgnjEIgqvFsdEX26lvi7ytkkUad9_Mm4LIs_-MxAnsoop3K0IFMzgq-IQ"
    HEADERS.update({'Authorization': f"Bearer {FIREANT_BEARER_TOKEN}"})
    
    FIREANT_API_ENDPOINT    = f"https://restv2.fireant.vn/symbols/{symbol}/full-financial-reports?"
    
    field_to_get = [
        { 'tongcongtaisan': 'totalAssets'},
        { 'taisancodinhhuuhinh': 'tangibleAssets'},
        { 'taisancodinhvohinh': 'intangibleAssets'},
        { 'doanhthuthuan': 'netRevenue'},
        { 'loinhuantruocthue': 'profitBeforeTaxes'},
        { 'loinhuansauthuecuacodongcuacongtyme': 'profitAfterTaxes'},
        { 'tonghangtonkho': 'inventory'},
        { 'nophaitra': 'liabilities'},
        { 'tienvatuongduongtiencuoiky': 'cashAndCashEquivalents'},
        { 'vonchusohuu': 'equity'},
        { 'nonganhan': 'shorttermLiabilities'},
        { 'nodaihan': 'longtermLiabilities'},
        { 'giavonhangban': 'costPrice'},
        { 'khauhaotscd': 'fixedAssetsDepreciation'},
        { 'trongdochiphilaivay': 'lendingCost'},
        { 'vayvanothuetaichinhnganhan': 'shorttermBorrowingsFinancialLeases'},
        { 'vayvanothuetaichinhdaihan': 'longtermBorrowingsFinancialLeases'},
    ]
    
    type_name = {
        1  : "candoiketoan" ,
        2  : "ketquakinhdoanh",
        3  : "luuchuyentientett",
        4  : "luuchuyentientegt"
    }
    
    for year in range(fromYear, toYear+1):
        for quarter in range(1, 4+1):
            if year == toYear and quarter > 1:
                break
            
            print(f"------------------- {symbol}/{year}/{quarter} -------------------")
            
            quarterInfo = {}
                                    
            for dict in field_to_get:
                quarterInfo.update({list(dict.values())[0] : 0})
            for statementType in range(1, 5):                    
                params = {
                    "type": statementType, 
                    "year": year,
                    "quarter": quarter,
                    "limit": 1,
                }
                
                fireant_response = requests.get(FIREANT_API_ENDPOINT, headers=HEADERS, params=params).json()
                
                try:
                    if (fireant_response != None):
                        for field in fireant_response:
                            if ('name' in field):
                                name =  removeSpace(cleanText(removeVietNameAccent(cleanBullet(cleanRoman(field['name']))))).lower()
                                value = field['values'][0]['value'] or 0
                                
                                for dict in field_to_get:
                                    if name in dict: quarterInfo.update({dict[name]: str(value)})
                    quarterInfo.update({f"year": year})
                    quarterInfo.update({f"quarter": quarter})
                except:
                    print(symbol + " ERROR" + year + " YEAR")
                    raise
            companyInfo.append(quarterInfo)
    return companyInfo

def populate_financialstatement(fromYear, toYear, upsert=False, verbose=False):

    company_list = Company.objects.all()
    start_time = time.time()
    financial_statement_column_list = [field.get_attname_column()[1]
                               for field in FinancialStatement._meta.fields[1:]]
    
    cursor = connection.cursor()
    row_cnt = 0
    sql = f"INSERT INTO stock_api_financialstatement ({','.join(financial_statement_column_list)}) VALUES "

    with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
    # Start the load operations and mark each future with its URL
        future_to_stock = {executor.submit(updateCompany, company.symbol , fromYear=fromYear, toYear=toYear): company for company in company_list}
        for future in concurrent.futures.as_completed(future_to_stock):
            symbol = future_to_stock[future].symbol
            companyInfo = future.result()
            for quarterInfo in companyInfo:
                financial_statement = [
                    symbol,
                    quarterInfo['year'],
                    quarterInfo['quarter'],
                    quarterInfo['totalAssets'],
                    quarterInfo['tangibleAssets'],
                    quarterInfo['intangibleAssets'],
                    quarterInfo['netRevenue'],
                    quarterInfo['profitBeforeTaxes'],
                    quarterInfo['profitAfterTaxes'],
                    quarterInfo['inventory'],
                    quarterInfo['liabilities'],
                    quarterInfo['cashAndCashEquivalents'],
                    quarterInfo['shorttermLiabilities'],
                    quarterInfo['longtermLiabilities'],
                    quarterInfo['costPrice'],
                    quarterInfo['equity'],
                    quarterInfo['fixedAssetsDepreciation'],
                    quarterInfo['lendingCost'],
                    quarterInfo['shorttermBorrowingsFinancialLeases'],
                    quarterInfo['longtermBorrowingsFinancialLeases']
                ]
                temp_sql = sql + ', '.join(['(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'])

                if upsert:
                    temp_sql += "AS new ON DUPLICATE KEY UPDATE {}".format(
                        ', '.join([f"{column} = new.{column}" for column in financial_statement_column_list]))

                # Batch insert all Financial_Statement records of a company
                try:
                    cursor.execute(temp_sql, financial_statement)
                    row_cnt += cursor.rowcount
                except Exception as e:
                    print(f"Exception: {str(e)}")
            print("Insert Financial Statement " + symbol + " success")

    if verbose:
        if upsert:
            print(f"TOTAL UPSERTED RECORDS: {row_cnt}")
        else:
            print(f"TOTAL INSERTED RECORDS: {row_cnt}")
        print(f"TIME ELAPSED: {str(time.time() - start_time)}")
        print("--FINISH INSERTING Financial_Statement TABLE--")
    
    cursor.close()


def run(*args):
    if args: 
        if args[0]:
            fromYear = args[0]
        if args[1]:
            toYear = args[1]
    else:
        fromYear = 2015
        toYear = 2022

    print("--BEGIN POPULATING Financial_Statement TABLE.--")

    print("TRUNCATING Financial_Statement TABLE.")
    with closing(connection.cursor()) as cursor:
        cursor.execute("TRUNCATE TABLE stock_api_financialstatement")

    # Get historical trades within input interval for each company
    populate_financialstatement(fromYear=fromYear, toYear=toYear, verbose=True)
