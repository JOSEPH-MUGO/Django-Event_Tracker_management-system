from django.urls import path
from .import views

urlpatterns = [
    #create event
    path('event/view/<int:id>/', views.view_event_by_id, name='viewEvent'),
    path('events/', views.viewEvents, name='viewEvents'),
    path('event/update',views.updateEvent, name='updateEvent'),
    path('event/delete/<int:id>/', views.deleteEvent, name='deleteEvent'),
    # create event category
    path('events/category/', views.eventCategory, name='createEventCategory'),


]
