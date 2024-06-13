from django.urls import path
from .import views

urlpatterns = [
    #create event
    path('event/view/', views.getEvent, name='getEvent'),
    path('events/', views.viewEvents, name='viewEvents'),
    path('event/update/',views.updateEvent, name='updateEvent'),
    path('event/delete/', views.deleteEvent, name='deleteEvent'),
    path('event/<int:event_id>/assignments', views.get_assignments, name='getAssignment'),
    path('employee/<int:employee_id>/assignments', views.getAssignments, name='getAssigned'),

    # create event category
    path('events/category/', views.eventCategory, name='createEventCategory'),
    path('event/category/', views.getCategory, name='getCategory'),
    path('event/category/update/', views.updateCategory, name='updateCategory'),
    path('event/category/delete/', views.deleteCategory, name='deleteCategory'),
    # assign event to employee
    path('assign/employee/view/', views.assign_employee, name='assignedEvent'),
    path('assign/get/assigned', views.getAssigned, name='getAssigned'),
    path('assign/update/', views.updateAssigned, name='updateAssigned'),
    path('assign/delete/', views.deleteAssigned, name='deleteAssigned'),
    

]
