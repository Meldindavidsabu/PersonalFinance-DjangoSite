# bills_receipts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('create/', views.document_create, name='document_create'),
    path('update/<int:pk>/', views.document_update, name='document_update'),
    path('delete/<int:pk>/', views.document_delete, name='document_delete'),
]
