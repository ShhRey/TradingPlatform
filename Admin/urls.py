from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterAdminView.as_view()),
    path('login', AdminLoginView.as_view()),
    path('view_profile', ViewProfileView.as_view()),
    path('add_market', AddMarketView.as_view()),
    path('add_exchange', AddExchangeView.as_view()),
    path('add_strategy', AddStrategyView.as_view()),
]
