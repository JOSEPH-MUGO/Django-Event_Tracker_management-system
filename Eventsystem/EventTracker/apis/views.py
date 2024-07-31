from rest_framework import viewsets
from .serializers import *
from EventRecord.models import *
from .permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class viewsetEmployee(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    
 
    def delete(self,request, *args, **kwargs):
        Employee.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class viewsetDepartment(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    
class viewsetEventCategory(viewsets.ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

class viewsetEvent(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]


class viewsetAssignment(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

   
        

class viewsetReport(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

