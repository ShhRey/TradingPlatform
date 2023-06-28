from django.urls import path
from .views import *

urlpatterns = [
    path('fetch_api_bal', LiveApiBalView.as_view()),
    path('get_api_bal', DBApiBalView.as_view()),
]