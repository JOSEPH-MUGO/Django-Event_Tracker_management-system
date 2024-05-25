from django.shortcuts import render,redirect,reverse
from .forms import EventForm
from .models import Event
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.db.models.functions import TruncWeek
from django.db.models import Count
from django.contrib import messages


# Create your views here.


def view_event_by_id(request, id):
    try:
        event = Event.objects.get(id=id)
        context = {
            'code': 200,
            'event_type': event.event_type,
            'title': event.title,
            'description': event.description,
            'venue': event.venue,
            'location': event.location,
            'start_date': event.start_date,
            'end_date': event.end_date,
            'id': event.id
        }
    except Event.DoesNotExist:
        context = {'code': 404}

    return JsonResponse(context)

def viewEvents(request):
    events = Event.objects.order_by('-title').all()
    form = EventForm(request.POST or None)
    context ={
        'events':events,
        'form1':form,
        'page_title':"Events"
    }
    if request.method == 'POST':
        if form.is_valid():
            form = form.save(commit=False)
            form.title = events.count()+1 #if it is empty
            form.save()
            messages.success(request,"New Event created ")
            return redirect(reverse('viewEvents'))
        else:
            messages.error(request, "Oops! Form error")

    return render(request, "EventRecord/create_event.html", context)



def updateEvent(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        instance = Event.objects.get(id=request.POST.get('id'))
        event = EventForm(request.POST or None, instance=instance)
        event.save()
        messages.success(request, "Event has been updated")
    except:
        messages.error(request, "Access To This Resource Denied")

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



