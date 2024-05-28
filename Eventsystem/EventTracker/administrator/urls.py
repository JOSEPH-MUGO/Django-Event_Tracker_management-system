from django.urls import path
from . import  views 

urlpatterns = [
    path('',views.admin_dashboard, name="admin_dashboard"),
    path('employees/',views.employees, name="adminViewEmployee"),
   
    path('employees/delete/<int:employee_id>/', views.deleteEmployee, name="deleteEmployee"),
    path('employees/update/<int:employee_id>/', views.updateEmployee, name="updateEmployee"),
    
]
