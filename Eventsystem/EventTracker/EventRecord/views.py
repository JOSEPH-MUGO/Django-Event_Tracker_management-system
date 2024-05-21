from django.shortcuts import render,redirect
from .forms import EventForm
from .models import Event

# Create your views here.

def create_event(request):
    if request.method == 'POST':
        form= EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'EventRecord/create_event.html', {'form':form})

def list_event(request):
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'EventRecord/event_list.html',context)
