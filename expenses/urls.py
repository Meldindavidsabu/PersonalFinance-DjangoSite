from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from .views import income_expense_dashboard

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('create/', views.expense_create, name='expense_create'),  # Expense creation
    path('edit/<int:pk>/', views.expense_edit, name='expense_edit'),
    path('delete/<int:pk>/', views.expense_delete, name='expense_delete'),
    path('export/csv/', views.export_expenses_csv, name='export_expenses_csv'),
    path('export/excel/', views.export_expenses_excel, name='export_expenses_excel'),
    path('export/pdf/', views.export_expenses_pdf, name='export_expenses_pdf'),
    path('income/', views.income_list, name='income_list'),
    path('income/create/', views.income_create, name='income_create'),  # Income creation
    path('income/edit/<int:pk>/', views.income_update, name='income_update'),
    path('income/delete/<int:pk>/', views.income_delete, name='income_delete'),
    path('income/export/csv/', views.export_income_csv, name='export_income_csv'),
    path('income/export/excel/', views.export_income_excel, name='export_income_excel'),
    path('income/export/pdf/', views.export_income_pdf, name='export_income_pdf'),
    path('export_to_email/', views.export_to_email, name='export_to_email'),
    path('expense/delete/<int:pk>/', views.expense_delete, name='expense_delete'),
    path('dashboard/', income_expense_dashboard, name='income_expense_dashboard'),




]
