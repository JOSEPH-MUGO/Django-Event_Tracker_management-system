from django.shortcuts import render,redirect,reverse,get_object_or_404
from .forms import *
from .models import *
from django_renderpdf.views import PDFView
from django.http import JsonResponse

from django.db.models import Count
from django.contrib import messages



# Create your views here.


def viewEvents(request):
    events = Event.objects.order_by('-id').all()
    category = EventCategory.objects.all()
    
    form = EventForm(request.POST or None)
    context ={
        'events': events,
        'form1': form,
        'category': category,
        'page_title': "Events"
    }
    if request.method == 'POST':
        if form.is_valid():
            form = form.save(commit=False)
           
            form.id = request.POST.get('id', events.count() + 1)  
            form.save()
            messages.success(request, "New Event created ")
            return redirect(reverse('viewEvents'))
        else:
            print(form.errors)
            messages.error(request, "Oops! Form error")

    return render(request, "EventRecord/create_event.html", context)

def listEvents(request):
    events = Event.objects.filter(status='active').order_by('-id')
    context ={
        'events': events,    
        'page_title': "All Active Events"
    }
    return render(request, "EventRecord/event_list.html", context)


def updateEvent(request, eventId=None):
    if eventId:
        event = get_object_or_404(Event, pk=eventId)
    else:
        messages.error(request, "Event ID is required")
        return redirect(reverse('viewEvents'))

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully")
            return redirect(reverse('viewEvents'))
        else:
            messages.error(request, "Form validation failed")
            for field in form:
                for error in field.errors:
                    print(f"Error in {field.label}: {error}")
    else:
        form = EventForm(instance=event)

    return render(request, 'EventRecord/edit_event.html', {
        'event': event,
        'form': form,
        'page_title': "Edit Event"
    })

def deleteEvent(request, eventId):
    event = get_object_or_404(Event, pk=eventId)
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, f"Event '{event.title}' deleted successfully")
        return redirect(reverse('viewEvents'))
    
    return render(request, 'EventRecord/delete_event.html', {
        'event': event,
        'page_title': "Delete Event"
    })


#create event category views
def eventCategory(request):
    category = EventCategory.objects.all()
    form = EventCategoryForm(request.POST or None)
    context = {'category': category,
               'form': form,
               'page_title':"Events Categories"
               }
    
    if request.method == 'POST':       
        if form.is_valid():
           form = form.save(commit=False)
           form.save()
           messages.success(request, "New category created successfully")
           return redirect(reverse('createEventCategory'))
        else:
            print(form.errors)
            messages.error(request,' Error occured!')
    return render(request, 'EventRecord/event_category.html', context)


def getCategory(request):
    category_id =request.GET.get('id')
    context = {}
    try:
        category = EventCategory.objects.get(id=category_id)
        context['code'] = 200
        context['id'] = category.id
        context['event_type'] = category.event_type
    except EventCategory.DoesNotExist:
        context['code'] =404
    return JsonResponse(context)

def updateCategory(request):
    if request.method != 'POST':
        messages.error(request, 'Access Denied!')
        return redirect(reverse('createEventCategory'))
    try:
        category_id = request.POST.get('id')
        category = EventCategory.objects.get(id =category_id)
        form = EventCategoryForm(request.POST or None, instance=category)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Event category updated!')
            return redirect(reverse('createEventCategory'))
    except EventCategory.DoesNotExist:
        messages.error(request, 'Event category not found')
        return redirect(reverse('createEventCategory'))
    
def deleteCategory(request):
    if request.method != 'POST':
        messages.error(request, 'Access denied')
        return redirect(reverse('createEventCategory'))
    try:
        category = EventCategory.objects.get(id = request.POST.get('id'))
        category.delete()
        messages.success(request, 'Event category deleted successfully')
        return redirect(reverse('createEventCategory'))
    except EventCategory.DoesNotExist:
        messages.error(request, 'Event Category not found')
        return redirect(reverse('createEventCategory'))

    #assigning employees the events



def assign_employee(request):
    assigns = Assignment.objects.all()
    if request.method == 'POST':
        department_id = request.POST.get('department')
        form = AssignForm(department_id=department_id, data=request.POST)
        if form.is_valid():
            event = form.cleaned_data['event']
            employee = form.cleaned_data['employee']
            assign_date = form.cleaned_data['assign_date']
            
            # Check if the employee is already assigned to an event on the same date
            if Assignment.objects.filter(employee=employee, event=event, assign_date=assign_date).exists():
                messages.error(request, 'Employee is already assigned another event on the same date.')
                return redirect(reverse('assignedEvent'))
            
            form.save()  # Ensure that assignment is only saved when form is valid
            messages.success(request, 'Employee assigned to the event successfully.')
            return redirect(reverse('assignedEvent'))
        else:
            messages.error(request, 'There was an error with your form. Please check the details.')
            return redirect(reverse('assignedEvent'))
    else:
        form = AssignForm()
    context = {
        'assigns': assigns,
        'form': form,
        'page_title': "Assigned Events"
    }
    return render(request, 'EventRecord/assign_event_employee.html', context)
def getAssigned(request):
    assign_id = request.GET.get('id')
    context = {}
    try:
        assign = Assignment.objects.get(id=assign_id)
        context['code'] = 200
        context['id'] = assign.id
        context['event'] = {
            'id': assign.event.id,
            'title': assign.event.title,
            'description': assign.event.description,
            'venue': assign.event.venue,
            'location': assign.event.location,
            'start_date': assign.event.start_date,
            'end_date': assign.event.end_date
        }
        context['department'] = {
            'id':assign.department.id,
            'name':assign.department.name
        }
        context['employee'] = {
            'id': assign.employee.id,
            'first_name': assign.employee.admin.first_name,
            'last_name': assign.employee.admin.last_name,
            'email': assign.employee.admin.email,
            'phone': assign.employee.phone
        }
        
        context['assign_date'] = assign.assign_date
        context['time'] = assign.time.strftime('%H:%M')
        context['message'] = assign.message
    except Assignment.DoesNotExist:
        context['code'] = 404
    return JsonResponse(context)


def updateAssigned(request):
    if request.method != 'POST':
        messages.error(request, 'Access Denied!')
        return redirect(reverse('assignedEvent'))
    
    try:
        assign_id = request.POST.get('id')
        assignments = get_object_or_404(Assignment, id=assign_id)
        department_id = assignments.department.id if assignments.department else None

        form = AssignForm(department_id=department_id, data=request.POST, instance=assignments)

        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment updated!')
            return redirect(reverse('assignedEvent'))
    except Assignment.DoesNotExist:
        messages.error(request, 'Assignment not found')
    
    return redirect(reverse('assignedEvent'))

def deleteAssigned(request):
    if request.method == 'POST':
        assign_id = request.POST.get('id')
        try:
            assignment = get_object_or_404(Assignment, id=assign_id)
            assignment.delete()
            messages.success(request, 'Assignment deleted successfully!')
        except Assignment.DoesNotExist:
            messages.error(request, 'Assignment not found.')
        return redirect(reverse('assignedEvent'))
    else:
        messages.error(request, 'Invalid request method.')
        return redirect(reverse('assignedEvent'))



def get_assignments(request, evenT_id):
    event = get_object_or_404(Event, pk=evenT_id)
    assignments = Assignment.objects.filter(event=event).select_related('employee')
    
    for assignment in assignments:
        assignment.report = Report.objects.filter(assignment_id=assignment.id).first()

    context = {
        'event': event,
        
        'assignments': assignments,
        'page_title': "View Event Assigment"
    }
    return render(request, 'EventRecord/view_assignment.html', context)

def getAssignments(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    assignments = Assignment.objects.filter(employee=employee).select_related('event')
    for assignment in assignments:
        assignment.report = Report.objects.filter(assignment_id=assignment.id).first()
    
    
    context = {
        'employee': employee,
        'assignments': assignments,        
        'page_title': "View Employee Assigment"
    }
    return render(request, 'EventRecord/view_employeeA.html', context)


