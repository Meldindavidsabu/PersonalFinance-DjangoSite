from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_goal, name='create_goal'),
    path('list/', views.goal_list, name='goal_list'),
    path('edit/<int:id>/', views.edit_goal, name='edit_goal'),
    path('delete/<int:id>/', views.delete_goal, name='delete_goal'),
    path('chart/', views.chart_view, name='chart_view'),  # Ensure this matches your view
    path('retirement-goals/', views.retirement_goal_list, name='retirement_goal_list'),

]
