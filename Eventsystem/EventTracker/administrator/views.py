from django.shortcuts import render, redirect, get_object_or_404
from account.forms import UserForm
from django.contrib import messages
#from django.http import JsonResponse, HttpResponseNotFound
from django.conf import settings
from EventRecord.models import *
from EventRecord.forms import *
from employee.models import Employee
from employee.forms import EmployeeForm
from django.db import IntegrityError,transaction
from django.core.mail import send_mail


# Create your views here.


def admin_dashboard(request):
    event_categories = EventCategory.objects.all()
    events = Event.objects.all()
    assignments = Assignment.objects.all()
    reports = Report.objects.all()
    report_files = ReportFile.objects.all()
    employee = Employee.objects.all()


    context = {
        
        'event_categories': event_categories,
        'events': events,
        'assignments': assignments,
        'reports': reports,
        'report_files': report_files,
        'event_category_count': event_categories.count(),
        'event_count': events.count(),
        'assignment_count': assignments.count(),
        'report_count': reports.count(),
        'report_file_count': report_files.count(),
        'employee_count':employee.count(),
        'page_title':"Dashboard"

    }
    return render(request, 'admin/adminV/home.html',context)


def employees(request):
    employees = Employee.objects.all()
    userForm = UserForm(request.POST or None)
    employeeForm = EmployeeForm(request.POST or None)
    context = {
        'form1': userForm,
        'form2': employeeForm,
        'employees': employees,
        'page_title': 'Employee List'
    }
    if request.method == 'POST':
        if userForm.is_valid() and employeeForm.is_valid():
            try:
                with transaction.atomic():
                    user, password = userForm.save(commit=False)
                    user.save()

                    employee = employeeForm.save(commit=False)
                    employee.admin = user
                    employee.email =user.email
                    employee.save()

                    send_mail(
                        'Your account credentials',
                        f'Your account has been created. Email: {user.email}, Password: {password}',
                        'josephithanwa@gmail.com',
                        [user.email],
                        fail_silently=False,
                    )

                    messages.success(request, "New employee created")
            except IntegrityError as e:
                if 'UNIQUE constraint' in str(e):
                    messages.error(request, "An employee with this email exist")
                else:
                    messages.error(request, "An error occured while creating the employee.")

        else:
            messages.error(request, "Form validation failed")
    return render(request, "admin/adminV/employee.html", context)



def updateEmployee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    user = employee.admin
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        employee_form = EmployeeForm(request.POST, instance=employee)
        if user_form.is_valid() and employee_form.is_valid():
            user_form.save()
            employee_form.save()
            messages.success(request, "Employee updated successfully")
            return redirect('adminViewEmployee')
    else:
        user_form = UserForm(instance=user)
        employee_form = EmployeeForm(instance=employee)
    return render(request, 'admin/adminV/edit_employee.html', {'user_form': user_form, 'employee_form': employee_form})


def deleteEmployee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, "Employee deleted successfully")
        return redirect('employee_list')
    return render(request, 'admin/adminVdelete_employee.html', {'employee': employee})



