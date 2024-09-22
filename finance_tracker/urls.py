from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
#from accounts import views as accounts_views
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication views (Django built-in)
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Expenses app URLs
    path('expenses/', include('expenses.urls')),

    # Accounts app URLs
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # For login

    # Retirement app URLs
    path('retirement/', include('retirement.urls')),

    # Other app URLs
    path('dues/', include('dues.urls')),
    path('reminders/', include('reminders.urls')),
    path('funds/', include('fund_integration.urls')),  
    path('notes/', include('notes.urls')),
    path('documents/', include('bills_receipts.urls')),
    path('currency/', include('currency.urls')),  



        




    # Home view (Redirect to login if not authenticated)
    path('', lambda request: redirect('login') if not request.user.is_authenticated else redirect('home')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

