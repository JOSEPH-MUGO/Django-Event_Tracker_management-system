from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name ='logout'),
    path('dashboard/',views.dashboard, name='dashboard'),
    #change password
    path('password_change/', auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #reseting password
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #path('', include('django.contrib.auth.urls)),
    path('register/',views.register, name='register'),
    
]
