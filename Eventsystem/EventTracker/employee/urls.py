from django.urls import path
from .import views

urlpatterns = [
    path('dashboard/',views.dashboard, name='dashboard'),

    path('department/',views.department, name="department"),
    path('department/view',views.getDepartment, name="getDepartment"),
    path('department/update',views.updateDepartment, name="updateDepartment"),
    path('department/delete',views.deleteDepartment, name="deleteDepartment"),
    path('get-employees-by-department/',views.getEmployeeDepartment, name='getEmployeeByDepartment'),
    path('employee/submit_report/<int:assign_id>/', views.submit_report, name='submitReport'),
    path('reports/submitted/',views.report,name='report')
]
