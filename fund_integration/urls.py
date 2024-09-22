from django.urls import path
from . import views
from .views import fetch_mutual_funds

urlpatterns = [
    path('mutual-funds/', views.fetch_mutual_funds, name='mutual_funds'),
    path('api/mutualfunds/', views.mutual_fund_api, name='mutual_fund_api'),
    path('mutual-funds/', fetch_mutual_funds, name='fetch_mutual_funds'),


]
