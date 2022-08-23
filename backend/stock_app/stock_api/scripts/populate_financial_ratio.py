from contextlib import closing
from django.db import connection

from ..models import FinancialRatio, FinancialStatement


def zero_division(n, d):
    return n / d if d else -1


def run(*args):

    print("--BEGIN POPULATING FINANCIAL_RATIO TABLE.--")

    print("TRUNCATING FINANCIAL_RATIO TABLE.")
    with closing(connection.cursor()) as cursor:
        cursor.execute("TRUNCATE TABLE stock_api_financialratio")

    financial_statements = FinancialStatement.objects.all()

    sql = f"""
    INSERT INTO stock_api_financialratio
    (company_id, year, quarter, return_on_equity, return_on_assets, return_on_invested_capitals,
     current_ratio, gross_margin, profit_margin, pretax_profit_margin )
    VALUES
    """
    rows = []

    for financial_statement in financial_statements:
        print(financial_statement.company.pk)
        rows.extend([
            financial_statement.company.pk,
            financial_statement.year,
            financial_statement.quarter,
            zero_division(financial_statement.profit_after_taxes,
                          financial_statement.equity),
            zero_division(financial_statement.profit_after_taxes,
                          financial_statement.total_assets),
            zero_division(financial_statement.profit_after_taxes,
                          financial_statement.equity +
                          financial_statement.longterm_borrowings_financial_leases),
            zero_division(financial_statement.total_assets,
                          financial_statement.liabilities),
            zero_division(financial_statement.net_revenue -
                          financial_statement.cost_price, financial_statement.net_revenue),
            zero_division(financial_statement.profit_after_taxes,
                          financial_statement.net_revenue),
            zero_division(financial_statement.profit_before_taxes,
                          financial_statement.net_revenue)
        ])

    sql += ', '.join(['(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)']
                                   * len(financial_statements))

    cursor = connection.cursor()
    
    try:
        cursor.execute(sql, rows)
    except Exception as e:
        print(f"Exception: {str(e)}")
    
    cursor.close()
    print("FINISH POPULATING FINANCIAL_RATIO TABLE.")
