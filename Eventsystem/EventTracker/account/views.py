from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'account/login.html'

class CustomLogoutView(LogoutView):
    template_name ='account/logout.html'
    next_page = reverse_lazy('login')

class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'account/reg.html'
    success_url = reverse_lazy('login')

    def get_queryset(self):
        return CustomUser.objects.none()

class DashboardView(TemplateView):
    template_name= 'dashboard.html'

class SidebarView(TemplateView):
    template_name = 'sidebar.html'

