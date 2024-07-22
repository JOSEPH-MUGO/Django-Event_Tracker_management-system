from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'department', viewsetDepartment)
router.register(r'employee', viewsetEmployee)
router.register(r'event_category', viewsetEventCategory)
router.register(r'events', viewsetEvent)
router.register(r'assignment', viewsetAssignment)
router.register(r'report', viewsetReport)

urlpatterns = [
    path('api/',include(router.urls))
]
