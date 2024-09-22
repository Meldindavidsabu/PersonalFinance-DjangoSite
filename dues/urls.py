from django.urls import path
from . import views

urlpatterns = [
    path('', views.due_list, name='due_list'),
    path('add/', views.add_due, name='add_due'),
    path('<int:due_id>/edit/', views.edit_due, name='edit_due'),
    path('<int:due_id>/delete/', views.delete_due, name='delete_due'),
    path('filter/', views.filter_dues, name='filter_dues'),
    path('notify/<int:due_id>/', views.notify_due, name='notify_due'),
    path('dashboard/', views.dashboard, name='dashboard'),



]
