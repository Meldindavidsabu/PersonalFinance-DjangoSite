from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('add/', views.add_reminder, name='add_reminder'),
    path('edit/<int:pk>/', views.edit_reminder, name='edit_reminder'),
    path('delete/<int:pk>/', views.delete_reminder, name='delete_reminder'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('reminders/', views.reminder_list, name='reminder_list'),
    path('reminders/add/', views.add_reminder, name='add_reminder'),
]
