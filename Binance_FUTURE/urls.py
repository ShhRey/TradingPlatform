from django.urls import path
from .views import *

urlpatterns = [
    path('fetch_api_bal', LiveApiBalView.as_view()),
    path('get_api_bal', DBApiBalView.as_view()),
    path('get_position_mode', GetPositionModeView.as_view()),
    path('change_position_mode', ChangePositionModeView.as_view()),
    path('get_asset_mode', GetAssetModeView.as_view()),
    path('change_asset_mode', ChangeAssetModeView.as_view()),
    path('open_orders', OpenOrderView.as_view()),
    path('order_history', OrderHistoryView.as_view()),
    path('limit_buy', LimitBuyOrderView.as_view()),
    path('limit_sell', LimitSellOrderView.as_view()),
    path('market_buy', MarketBuyOrderView.as_view()),
    path('market_sell', MarketSellOrderView.as_view()),
    path('cancel_order', CancelOpenOrderView.as_view()),
]