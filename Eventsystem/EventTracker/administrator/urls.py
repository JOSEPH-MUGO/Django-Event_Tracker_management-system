from django.urls import path
from . import  views 

urlpatterns = [
    path('',views.admin_dashboard, name="admin_dashboard"),
    path('employees/',views.employees, name="adminViewEmployee"),
    path('employee/view', views.get_employee, name='getEmployee'),
    path('employees/delete', views.deleteEmployee, name="deleteEmployee"),
    path('employees/update', views.updateEmployee, name="updateEmployee"),
    
]
