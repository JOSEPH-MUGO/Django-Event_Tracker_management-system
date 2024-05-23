from django.shortcuts import render, reverse, redirect
from account.forms import CustomUserForm
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from EventRecord.models import *
from EventRecord.forms import *



# Create your views here.


def admin_dashboard(request):
    event_categories = EventCategory.objects.all()
    events = Event.objects.all()
    assignments = Assignment.objects.all()
    reports = Report.objects.all()
    report_files = ReportFile.objects.all()


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
    }
    return render(request, 'admin/adminV/home.html',context)



