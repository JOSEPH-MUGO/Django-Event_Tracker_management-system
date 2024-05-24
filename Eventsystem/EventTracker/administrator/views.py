from django.shortcuts import render, reverse, redirect, get_object_or_404
from account.forms import CustomUserForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponseNotFound
from django.conf import settings
from EventRecord.models import *
from EventRecord.forms import *
from employee.models import Employee
from employee.forms import EmployeeForm
from django.db import IntegrityError,transaction



# Create your views here.


def admin_dashboard(request):
    event_categories = EventCategory.objects.all()
    events = Event.objects.all()
    assignments = Assignment.objects.all()
    reports = Report.objects.all()
    report_files = ReportFile.objects.all()
    employee = CustomUser.objects.all()


    context = {
        'page_tittle':'Dashboard',
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
        'employee_count':employee.count()
    }
    return render(request, 'admin/adminV/home.html',context)


def employees(request):
    employees = Employee.objects.all()
    userForm = CustomUserForm(request.POST or None)
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
                    user = userForm.save(commit=False)
                    user.save()

                    employee = employeeForm.save(commit=False)
                    employee.admin = user
                    employee.email =user.email
                    employee.save()

                    messages.success(request, "New employee created")
            except IntegrityError as e:
                if 'UNIQUE constraint' in str(e):
                    messages.error(request, "An employee with this email exist")
                else:
                    messages.error(request, "An error occured while creating the employee.")

        else:
            messages.error(request, "Form validation failed")
    return render(request, "admin/adminV/employee.html", context)



def view_employee_by_id(request):
    employee_id = request.GET.get('id', None)
    context = {}

    if not employee_id:
        context['code'] = 400
        context['message'] = 'Bad Request: Employee ID is required.'
        return JsonResponse(context, status=400)

    try:
        employee = get_object_or_404(Employee, id=employee_id)

        context['code'] = 200
        context['id'] = employee.id
        context['first_name'] = employee.admin.first_name
        context['last_name'] = employee.admin.last_name
        context['phone'] = employee.phone
        
        context['email'] = employee.admin.email
        
    except:
        context['code'] = 404
        context['message'] = 'Employee not found.'
        return HttpResponseNotFound()

    return JsonResponse(context)
def updateEmployee(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
        return redirect(reverse('adminViewEmployee'))

    try:
        employee_id = request.POST.get('id')
        instance = get_object_or_404(Employee, id=employee_id)
        user_form = CustomUserForm(request.POST, instance=instance.admin)
        employee_form = EmployeeForm(request.POST, instance=instance)

        if user_form.is_valid() and employee_form.is_valid():
            user_form.save()
            employee_form.save()
            messages.success(request, "Employee updated")
        else:
            messages.error(request, "Form validation failed")
    except Employee.DoesNotExist:
        messages.error(request, "Employee does not exist")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect(reverse('adminViewEmployee'))

def deleteEmployee(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
        return redirect(reverse('adminViewEmployee'))

    try:
        employee_id = request.POST.get('id')
        employee = get_object_or_404(Employee, id=employee_id)
        employee.admin.delete()  
        messages.success(request, "Employee has been deleted")
    except Employee.DoesNotExist:
        messages.error(request, "Employee does not exist")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect(reverse('adminViewEmployee'))


