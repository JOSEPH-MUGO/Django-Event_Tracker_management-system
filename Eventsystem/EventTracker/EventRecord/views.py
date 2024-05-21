from django.shortcuts import render,redirect
from .forms import EventForm
from .models import Event
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.db.models.functions import TruncWeek
from django.db.models import Count


# Create your views here.

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
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

def event_chart(request):
    weekly = (
        Event.objects.annotate(week=TruncWeek('start_date')).values('week').annotate(event_count=Count('id')).order_by('week')

    )
    data = { 
        'weeks':[entry['week'].strftime('%Y-%m-%d') for entry in weekly],
        'event_counts':[entry['event_count'] for entry in weekly]

    }
    return JsonResponse(data)









