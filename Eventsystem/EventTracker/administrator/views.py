from django.shortcuts import render,reverse, redirect
from account.forms import UserForm
from django.contrib import messages
from django.http import JsonResponse
from EventRecord.models import *
from EventRecord.forms import *
from employee.models import Employee,Department
from employee.forms import EmployeeForm
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import PermissionsMixin


# Create your views here.


def admin_dashboard(request):
    event_categories = EventCategory.objects.all()
    events = Event.objects.all()
    assignments = Assignment.objects.all()
    reports = Report.objects.all()
    report_files = ReportFile.objects.all()
    employee = Employee.objects.all()
    department =Department.objects.all()


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
        'department_count':department.count(),
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
            user,password = userForm.save(commit=False)
            user.save()

            employee = employeeForm.save(commit=False)
            employee.admin = user
            employee.admin.email =user.email
            employee.save()

            send_mail(
                'Your account credentials',
                f' Hello! {user.first_name}, Your account for Event Tracker Management System has been created successfull  using this Email: {user.email},Use this  Password: {password} to login into the system, Thanks',
                'josephithanwa@gmail.com',
                [user.email],
                fail_silently=False,
             )

            messages.success(request, "New employee created")

        else:
            messages.error(request, "Form validation failed")
    return render(request, "admin/adminV/employee.html", context)


def get_employee(request):
    employee_id = request.GET.get('id', None)
    context = {}
    try:
        employee = Employee.objects.get(id=employee_id)
        context['code'] = 200
        context['first_name'] = employee.admin.first_name
        context['last_name'] = employee.admin.last_name
        context['email'] = employee.admin.email
        context['phone'] = employee.phone
        context['id'] = employee.id
    except Employee.DoesNotExist:
        context['code'] = 404
    return JsonResponse(context)



def updateEmployee(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        instance = Employee.objects.get(id=request.POST.get('id'))      
        user = instance.admin
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        employee = EmployeeForm(request.POST or None, instance=instance)
        if employee.is_valid():  # Check for valid phone number format (optional)
            employee.save()
        else:
            messages.error(request, f"Invalid phone number format. {employee.errors['phone']}")

        employee.save()
        messages.success(request, "Employee updated")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('adminViewEmployee'))



def deleteEmployee(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        

        employee = Employee.objects.get(id = request.POST.get('id')).admin
        employee.delete()
        messages.success(request, 'Employee deleted successfully')
    except:
        messages.error(request, 'You can not delete the employee')

        
    return redirect(reverse('adminViewEmployee'))

def get_assignments(request):
    employee_id = request.GET.get('id')
    context = {}
    try:
        employee = Employee.objects.get(id = employee_id)
        # Fetch assignments based on the employee ID
        assignments = Assignment.objects.filter(employee=employee)
        # Convert assignments to a list of dictionaries with event title
        assignments_list = [{'title': assignment.event.title, 'start_date': assignment.assign_date,
                             'employee_first_name': assignment.employee.admin.first_name,
                             'employee_last_name': assignment.employee.admin.last_name} for assignment in assignments]
        context['code'] =200
        context['assignments'] = assignments_list
       
    except Employee.DoesNotExist:
        context['code'] = 404
        context['message'] = 'Employee not found'
    return JsonResponse(context)