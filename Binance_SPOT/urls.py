from django.urls import path
from .views import *

urlpatterns = [
    path('fetch_api_bal', LiveApiBalView.as_view()),
    path('get_api_bal', DBApiBalView.as_view()),
    path('open_orders', OpenOrderView.as_view()),
    path('order_history', OrderHistoryView.as_view()),
    path('limit_buy', LimitBuyOrderView.as_view()),
    path('limit_sell', LimitSellOrderView.as_view()),
    path('market_buy', MarketBuyOrderView.as_view()),
    path('market_sell', MarketSellOrderView.as_view()),
    path('modify_order', ModifyOrderView.as_view()),
    path('cancel_order', CancelOpenOrderView.as_view()),
    path('cancel_all_open', CancelAllOpenOrdersView.as_view()),
]