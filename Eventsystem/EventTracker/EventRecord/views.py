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
"""
def getEvent(request):
    event_id = request.GET.get('id',None)
    event = Event.objects.filter(id=event_id)
    context = {}
    if not event.exists():
        context['code'] = 404
    else:
        context['code'] = 200
        context['id'] = event.id
        context['event_type'] = event.event_type.id
        context['title'] = event.title
        context['description'] = event.description
        context['venue'] = event.venue
        context['location'] = event.location
        context['start_date'] = event.start_date
        context['end_date'] = event.end_date
    return JsonResponse(context)

"""
def getEvent(request):
    event_id = request.GET.get('id')
    context = {}
    try:
        event = Event.objects.get(id=event_id)
        context['code'] = 200
        context['id'] = event.id
        context['event_type'] = event.event_type.id # Assuming event_type is a ForeignKey
        context['title'] = event.title
        context['description'] = event.description
        context['venue'] = event.venue
        context['location'] = event.location
        context['start_date'] = event.start_date.strftime('%Y-%m-%d')  # Format date
        context['end_date'] = event.end_date.strftime('%Y-%m-%d')      # Format date
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







"""
def getEvent(request):
    event_id = request.GET.get('id')
    print(f"Received request for event ID:{event_id}")
    if event_id is None:
        return JsonResponse({'code': 400, 'message': 'Event ID not provided '}, status =400)    
    try:
        event = Event.objects.get(pk=event_id)
        data ={
            'code': 200,
            'event_type': event.event_type.id,  # Use ID to set in the dropdown
            'title': event.title,
            'description': event.description,
            'venue': event.venue,
            'location': event.location,
            'start_date': event.start_date.strftime('%Y-%m-%d'),
            'end_date': event.end_date.strftime('%Y-%m-%d'),
            'id': event.id
            
        }
        print(f"Returning event data:{data}")
        return JsonResponse(data)
    except Event.DoesNotExist:
         print(f"Event with ID {event_id} does not exist")

        
         return JsonResponse({'code': 404, 'message':'Event not found'}, status = 404)
"""

"""
def updateEvent(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
        return redirect(reverse('viewEvents'))
    event_id = request.POST.get('id')
    instance = get_object_or_404(Event, id=event_id)
    form = EventForm(request.POST, instance=instance)

    if form.is_valid():
        form.save()
        messages.success(request, "Event has been updated")
    else:
        messages.error(request, "Form is invalid")
        print(form.errors)  

    return redirect(reverse('viewEvents'))

def deleteEvent(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        event = Event.objects.get(id=request.POST.get('id'))
        event.delete()
        messages.success(request, "Event Has Been Deleted")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('viewEvents'))

"""
   

    

#create event category views
def eventCategory(request):
    category = EventCategory.objects.all()
    form = EventCategoryForm(request.POST or None)
    context = {'category': category,
               'form': form,
               'page_title':"Event Category"
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
