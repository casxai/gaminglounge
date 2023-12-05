from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('edit-profile/changepassword/', views.change_password, name='change_password')
    # path('getChartData/', views.get_chart_data, name='get_chart_data'),
    # path('get_weekly_data/', views.get_weekly_data, name="get_weekly_data"),
    # path('get_monthly_data/', views.get_monthly_data, name="get_monthly_data"),
]