from django.urls import path
from .import views

urlpatterns = [
    path('event/view/<int:id>/', views.view_event_by_id, name='viewEvent'),
    path('events/', views.viewEvents, name='viewEvents'),
    path('event/update',views.updateEvent, name='updateEvent'),
    path('event/delete', views.deleteEvent, name='deleteEvent'),


]
