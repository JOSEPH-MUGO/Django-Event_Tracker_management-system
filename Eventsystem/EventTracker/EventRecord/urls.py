from django.urls import path
from .import views

urlpatterns = [
    path('create_event/', views.create_event, name='create_event'),
    path('event_list/', views.list_event, name='event_list'),

]
