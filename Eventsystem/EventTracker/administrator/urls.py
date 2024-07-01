from django.urls import path
from . import  views 


urlpatterns = [
    path('',views.admin_dashboard, name="admin_dashboard"),
    path('employees/',views.employees, name="adminViewEmployee"),
    path('employee/view', views.get_employee, name='getEmployee'),
    path('employees/delete', views.deleteEmployee, name="deleteEmployee"),
    path('employees/update', views.updateEmployee, name="updateEmployee"),
    path('get-assignments/', views.get_assignments, name='getAssignments'),
    path('download_report_pdf/<int:report_id>/', views.ReportPDFView.as_view(), name='downloadReport'),
  
]
