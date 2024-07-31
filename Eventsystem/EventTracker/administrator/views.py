from django.shortcuts import render,reverse, redirect,get_object_or_404
from account.forms import UserForm
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
from EventRecord.models import *
from EventRecord.forms import *
from employee.models import Employee,Department
from employee.forms import EmployeeForm
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags

from xhtml2pdf import pisa
from django.conf import settings

# Create your views here.


def admin_dashboard(request):
    event_categories = EventCategory.objects.all()
    events = Event.objects.all().annotate(employee_count=models.Count('assignment')).values('title', 'employee_count')
    assignments = Assignment.objects.all()
    reports = Report.objects.all()
    employees = Employee.objects.all()
    departments = Department.objects.all()

    # Aggregate event counts per category
    category_event_counts = [
        {
            'category': category.event_type,
            'event_count': events.filter(event_type=category).count()
        } for category in event_categories
    ]

    context = {
        'event_categories': category_event_counts,
        'events': events,
        'assignments': assignments,
        'reports': reports,
        'event_category_count': event_categories.count(),
        'event_count': events.count(),
        'assignment_count': assignments.count(),
        'report_count': reports.count(),
        'employee_count': employees.count(),
        'department_count': departments.count(),
        'page_title': "Dashboard"
    }
    return render(request, 'admin/adminV/home.html', context)

def employees(request):
    employees = Employee.objects.all()
    departments = Department.objects.all()
    userForm = UserForm(request.POST or None)
    employeeForm = EmployeeForm(request.POST or None)
    context = {
        'form1': userForm,
        'form2': employeeForm,
        'departments':departments,
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
        department = {
            'id': employee.department.id,
            'name': employee.department.name,
        }
        context['department'] = department
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


#Download and view the pdf


def downloadReport(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    template_path = 'report/report_pdf.html'  # Path to your HTML template

    context = {
        'report': report,
    }

    # Rendered template
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="report_{report_id}.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response    


def batch_approve_reports(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        report_ids = request.POST.getlist('reports')

        if not status or not report_ids:
            messages.error(request, 'Please select a status and at least one report.')
            return redirect('report')

        for report_id in report_ids:
            try:
                report = Report.objects.get(id=report_id)
                if report.status == 'approved':
                    continue  # Skip if already approved

                report.status = status
                report.save()

                if status == 'approved':
                    # Send email notification to the report owner
                    subject = 'Your Report Has Been Approved'
                    email_content = render_to_string('emails/report_approval_email.html', {'report': report})
                    plain_message = strip_tags(email_content)
                    
                    send_mail(subject, plain_message, '', [report.submitted_by.admin.email], fail_silently=False)

            except Report.DoesNotExist:
                continue  # Skip if report does not exist

        messages.success(request, f'Reports have been {status} successfully.')
        return redirect('report')
    else:
        return redirect('report')
    
def notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    context = {
        'notifications': notifications,
        'unread_notifications_count': notifications.count(),
    }
    return render(request, 'EventRecord/notification.html', context)