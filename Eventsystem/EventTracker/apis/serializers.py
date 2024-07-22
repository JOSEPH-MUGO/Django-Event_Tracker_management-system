from rest_framework import serializers
from EventRecord.models import *
from employee.models import Department,Employee
from account.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
import random
import string

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= EventCategory
        fields= '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Event
        fields ='__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['content','image']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['last_name','first_name','email']
    

    def create(self, validated_data):
        # Generate a random password
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        validated_data['password'] = make_password(password)

        user = User.objects.create(**validated_data)

        # Send email with password
        send_mail(
           'Your account credentials',
            f' Hello! {user.first_name}, Your account for Event Tracker Management System has been created successfull  using this Email: {user.email},Use this  Password: {password} to login into the system, Thanks',
            'josephithanwa@gmail.com',  # sender email
            [user.email],
            fail_silently=False,
        )

        return user

class EmployeeSerializer(serializers.ModelSerializer):
    admin = UserSerializer()
    class Meta:
        model = Employee
        fields = ['admin', 'phone', 'department']
    
    def create(self, validated_data):
        user_data = validated_data.pop('admin')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        employee = Employee.objects.create(admin=user, **validated_data)
        return employee

    def update(self, instance, validated_data):
        user_data = validated_data.pop('admin')
        user = instance.admin

        # Update User fields
        user_serializer = UserSerializer(user, data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        # Update Employee fields
        instance.phone = validated_data.get('phone', instance.phone)
        instance.department = validated_data.get('department', instance.department)
        instance.save()

        return instance
        