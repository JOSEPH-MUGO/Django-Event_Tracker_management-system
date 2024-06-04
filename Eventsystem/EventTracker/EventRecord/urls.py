from django.urls import path
from .import views

urlpatterns = [
    #create event
    path('event/view/', views.getEvent, name='getEvent'),
    path('events/', views.viewEvents, name='viewEvents'),
    path('event/update/',views.updateEvent, name='updateEvent'),
    path('event/delete/', views.deleteEvent, name='deleteEvent'),
    # create event category
    path('events/category/', views.eventCategory, name='createEventCategory'),
]
