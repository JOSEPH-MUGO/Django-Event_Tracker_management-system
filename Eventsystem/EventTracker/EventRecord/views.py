from django.shortcuts import render,redirect,reverse,get_object_or_404
from .forms import *
from .models import *
from django.http import JsonResponse

from django.db.models import Count
from django.contrib import messages



# Create your views here.


def viewEvents(request):
    events = Event.objects.order_by('-id').all()
    category = EventCategory.objects.all()
    
    form = EventForm(request.POST or None)
    context ={
        'events':events,
        'form1':form,
        'category':category,
        'page_title':"Events"
    }
    if request.method == 'POST':
        if form.is_valid():
            form = form.save(commit=False)
            form.id= request.POST.get('id',events.count()+1) #if it is empty
            form.save()
            messages.success(request,"New Event created ")
            return redirect(reverse('viewEvents'))
        else:
            print(form.errors)
            messages.error(request, "Oops! Form error")

    return render(request, "EventRecord/create_event.html", context)

def getEvent(request):
    event_id = request.GET.get('id')
    context = {}
    try:
        event = Event.objects.get(id=event_id)
        context['code'] = 200
        context['id'] = event.id
        context['event_type'] = event.event_type.id # event_type is a ForeignKey
        context['title'] = event.title
        context['description'] = event.description
        context['venue'] = event.venue
        context['location'] = event.location
        context['start_date'] = event.start_date.strftime('%Y-%m-%d') 
        context['end_date'] = event.end_date.strftime('%Y-%m-%d')      
    except Event.DoesNotExist:
        context['code'] = 404
    return JsonResponse(context)

def updateEvent(request ):
    if request.method != 'POST':
        messages.error(request, "Access denied")
        return redirect(reverse('viewEvents'))
    try:  
        event_id =request.POST.get('id')
        event = Event.objects.get(id=event_id)
        form = EventForm(request.POST or None, instance=event)

        if form.is_valid():
           form.save()
           messages.success(request, "Event updated successfully")
        else:
            messages.error(request, "Form validation failed")
            print(form.errors)
    except Event.DoesNotExist:
        messages.error(request, "Event not found")
    except Exception as e:
        messages.error(request, f"Unexpected Problem Occured:{str(e)}")
    return redirect(reverse('viewEvents'))
            
def deleteEvent(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
        return redirect(reverse('viewEvents'))
    try:
        event= Event.objects.get(id=request.POST.get('id'))
        event.delete()
        messages.success(request, "Event delete successfully")
    except Event.DoesNotExist:
        messages.error(request, "Event not found")
   
    return redirect('viewEvents') 



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
        form = AssignForm(request.POST)
        if form.is_valid():
            event = form.cleaned_data['event']
            employee = form.cleaned_data['employee']
            assign_date = form.cleaned_data['assign_date']
            
            # Check if the employee is already assigned to an event on the same date
            if Assignment.objects.filter(employee=employee, event=event, assign_date=assign_date).exists():
                messages.error(request, 'Employee is already assigned another event on the same date.')
                return redirect(reverse('assignedEvent'))
            
            form.save()
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
        context['employee'] = {
            'id': assign.employee.id,
            'first_name': assign.employee.admin.first_name,
            'last_name': assign.employee.admin.last_name,
            'email': assign.employee.admin.email,
            'phone': assign.employee.phone
        }
        
        context['assign_date'] = assign.assign_date
        context['time'] = assign.time.strftime('%H:%M')
    except Assignment.DoesNotExist:
        context['code'] = 404
    return JsonResponse(context)

def updateAssigned(request):
    if request.method != 'POST':
        messages.error(request, 'Access Denied!')
        return redirect(reverse('assignedEvent'))
    try:
        assign_id = request.POST.get('id')
        assignments = Assignment.objects.get(id =assign_id)
       
        form = AssignForm(request.POST or None, instance=assignments)
        
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Assigment updated!')
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


def get_assignments(request):
    event_id = request.GET.get('id')
    try:
        
        assignments = Assignment.objects.filter(event_id=event_id)
        
        assignments_list = [{
            'id': assignment.id,
            'title': assignment.event.title,
            'start_date': assignment.assign_date,
            'assign_time': assignment.time,
            'employee': {
                'first_name': assignment.employee.admin.first_name if assignment.employee else None,
                'last_name': assignment.employee.admin.last_name if assignment.employee else None
            }
        } for assignment in assignments]
        return JsonResponse({'code': 200, 'assignments': assignments_list})
    except Assignment.DoesNotExist:
        return JsonResponse({'code': 404, 'message': 'Assignments not found'})
