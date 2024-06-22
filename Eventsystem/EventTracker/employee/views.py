from django.shortcuts import render,redirect, get_object_or_404,reverse
from EventRecord.models import *
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from EventRecord.forms import ReportForm
from io import BytesIO
from reportlab.pdfgen import canvas
import os
from django.utils.html import strip_tags
from . models import *
from . forms import *
from django.http import JsonResponse,HttpResponse,FileResponse
# Create your views here.

# employee dashboard
def dashboard(request):
  user = request.user
  assignments = Assignment.objects.filter(employee=user.employee)
  if user.is_authenticated and user.user_type == '2':
    context = {
        'assignments': assignments,
        'page_title':"Employee Dashboard"
    }
    return render(request, 'account/employee_home.html', context)



def department(request):
    departments = Department.objects.all()
    form = DepartmentForm(request.POST or None)
    context = {'departments': departments,
               'form': form,
               'page_title':"Departments"
               }
    
    if request.method == 'POST':       
        if form.is_valid():
           form = form.save(commit=False)
           form.save()
           messages.success(request, "New department created successfully")
           return redirect(reverse('department'))
        else:
            print(form.errors)
            messages.error(request,' Error occured!')
    return render(request, 'EventRecord/department.html', context)


def getDepartment(request):
    department_id =request.GET.get('id')
    context = {}
    try:
        department = Department.objects.get(id=department_id)
        context['code'] = 200
        context['id'] = department.id
        context['name'] = department.name
        context['created_at'] = department.created_at.strftime('%Y-%m-%dT%H:%M')

    except Department.DoesNotExist:
        context['code'] =404
    return JsonResponse(context)

def updateDepartment(request):
    if request.method != 'POST':
        messages.error(request, 'Access Denied!')
        return redirect(reverse('department'))
    try:
        department_id = request.POST.get('id')
        department = Department.objects.get(id =department_id)
        form = DepartmentForm(request.POST or None, instance=department)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfull')
            return redirect(reverse('department'))
    except Department.DoesNotExist:
        messages.error(request, 'Department not found')
        return redirect(reverse('department'))
    
def deleteDepartment(request):
    if request.method != 'POST':
        messages.error(request, 'Access denied')
        return redirect(reverse('department'))
    department_id = request.POST.get('id')
    try:
        department = Department.objects.get(id = department_id)
        department.delete()
        messages.success(request, 'Department deleted successfully')
        return redirect(reverse('department'))
    except Department.DoesNotExist:
        messages.error(request, 'Department not found')
        return redirect(reverse('department'))


def getEmployeeDepartment(request):
    department_id = request.GET.get('department_id')
    employees = Employee.objects.filter(department_id=department_id).values('id', 'admin__first_name', 'admin__last_name','admin__email')
    employee_list = list(employees)
    return JsonResponse(employee_list, safe=False)



def submit_report(request, assign_id=None):
    assignment = None
    assigned = False
    report_form = None

    # Fetch the most recent assignment for the logged-in employee
    if request.user.is_authenticated and assign_id is None:
        assignments = Assignment.objects.filter(employee=request.user.employee).order_by('-assign_date')
        if assignments.exists():
            assignment = assignments.first()
            assigned = True
    elif assign_id:
        try:
            assignment = Assignment.objects.get(id=assign_id, employee=request.user.employee)
            assigned = True
        except Assignment.DoesNotExist:
            assigned = False

    if assigned:
        if request.method == 'POST':
            report_form = ReportForm(request.POST,request.FILES)
            if report_form.is_valid():
                report = report_form.save(commit=False)
                report.assignment = assignment
                report.submitted_by = assignment.employee
                report.save()           
                messages.success(request, 'Report submitted successfully.')
                return redirect('dashboard')  # Replace with your appropriate URL
            else:
                messages.error(request, 'Error submitting report. Please check the form.')
        else:
            report_form = ReportForm()
    else:
        messages.error(request, 'No assignment found or you are not authorized to submit this report.')

    context = {
        'assignment': assignment,
        'report_form': report_form,
        'page_title': "Create Report",
        'assigned': assigned
    }
    return render(request, 'report/submit_report.html', context)
def report(request):
    reports = Report.objects.all()
    context ={'reports':reports,'page_title':"Submited Reports"}
    return render(request, 'EventRecord/report_assign.html',context)