from django.urls import path, re_path
from .views import CompanyViewSet, MarketPriceViewSet, StockPriceViewSet, FinancialStatementViewSet, FinancialRatioViewSet, BusinessValuationViewSet, StockValuationViewSet

urlpatterns = [
    path('company', CompanyViewSet.as_view({
        'get': 'list'
    })),
    path('company/<slug:pk>', CompanyViewSet.as_view({
        'get': 'retrieve'
    })),
    path('market-price', MarketPriceViewSet.as_view({
        'get': 'list'
    })),
    path('stock-price', StockPriceViewSet.as_view({
        'get': 'list'
    })),
    path('stock-price/top-foreign-value', StockPriceViewSet.as_view({
        'get': 'get_top_total_foreign'
    })),
    path(r'stock-price/<slug:company>', StockPriceViewSet.as_view({
        'get': 'get_company_stock_price_history'
    })),
    path(r'stock-price/all/<slug:trading_date>', StockPriceViewSet.as_view({
        'get': 'get_stock_price_history_group_by_industry'
    })),
    path('financial-statements', FinancialStatementViewSet.as_view({
        'get': 'list'
    })),
    path(r'financial-statements/<slug:company>', FinancialStatementViewSet.as_view({
        'get': 'get_stock_financial_statement'
    })),
    path('financial-ratio', FinancialRatioViewSet.as_view({
        'get': 'list'
    })),
    path(r'financial-ratio/<slug:company>', FinancialRatioViewSet.as_view({
        'get': 'get_stock_financial_ratio'
    })),
    path('business-valuation', BusinessValuationViewSet.as_view({
        'get': 'list'
    })),
    path(r'business-valuation/<slug:company>', BusinessValuationViewSet.as_view({
        'get': 'get_stock_business_valuation'
    })),
    path(r'industry-valuation', StockValuationViewSet.as_view({
        'get': 'list'
    })),
    path(r'industry-valuation/<slug:company>', StockValuationViewSet.as_view({
        'get': 'get_stock_valuation'
    }))
]
