from django.urls import path
from .views import CustomLoginView, CustomLogoutView,CustomRegisterView,DashboardView, SidebarView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login' ),
    path('logout/', CustomLogoutView.as_view(),name='logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(),name='dashboard'),
    path('sidebar/', SidebarView.as_view(), name='sidebar'),
]
