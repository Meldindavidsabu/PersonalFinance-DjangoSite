# accounts/urls.py
from django.urls import path
from . import views
from .views import home

urlpatterns = [
    # Define your account-related URLs here
    path('', home, name='home'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    #path('profile/', views.profile, name='profile'),
    # Add other account-related paths as needed
]
