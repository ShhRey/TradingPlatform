from django.urls import path
from .views import *

urlpatterns = [
    path('add_market', AddMarketView.as_view()),
    path('add_exchange', AddExchangeView.as_view()),
    path('add_api', AddApiView.as_view()),
]
