from django.urls import path
from .import views

urlpatterns = [

    path('department/',views.department, name="department"),
    path('department/view',views.getDepartment, name="getDepartment"),
    path('department/update',views.updateDepartment, name="updateDepartment"),
    path('department/delete',views.deleteDepartment, name="deleteDepartment"),
      path('get-employees-by-department/',views.getEmployeeDepartment, name='getEmployeeByDepartment'),
]
