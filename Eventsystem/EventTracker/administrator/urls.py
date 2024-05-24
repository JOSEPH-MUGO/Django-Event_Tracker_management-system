from django.urls import path
from . import  views 

urlpatterns = [
    path('',views.admin_dashboard, name="admin_dashboard"),
    path('employees/',views.employees, name="adminViewEmployee"),
    path('employee/view', views.view_employee_by_id, name="viewEmployee"),
    path('employee/delete', views.deleteEmployee, name="deleteEmployee"),
    path('employee/update/', views.updateEmployee, name="updateEmployee"),
    
]
