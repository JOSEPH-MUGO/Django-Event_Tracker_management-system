from django.shortcuts import render,redirect, get_object_or_404,reverse
from EventRecord.models import *
from EventRecord.forms import ReportForm
from django.contrib import messages
from . models import *
from . forms import *
from django.http import JsonResponse
# Create your views here.


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







def submitReport(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, employee=request.user.employee)
    
    if request.method =='POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.assignment = assignment
            report.event = assignment.event
            report.employee = request.user.employee
            report.save()
            messages.success(request, 'Report submitted successfully.')
            return redirect('event_detail', event_id=assignment.event.id)
    else:
        form = ReportForm()
    return render(request, 'submit_report.html', {'form': form, 'assignment': assignment})

        

