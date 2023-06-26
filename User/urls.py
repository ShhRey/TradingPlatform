from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterUserView.as_view()),
    path('login', UserLoginView.as_view()),
    path('view_profile', ViewProfileView.as_view()),
    path('update_profile', UpdateProfileView.as_view()),
    path('add_api', AddApiView.as_view()),
]
