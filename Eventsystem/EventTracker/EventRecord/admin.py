from django.contrib import admin
from .models import Event
# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_type','title','description','venue','location','start_date','end_date')
    search_fields= ('title','event_type','location')

