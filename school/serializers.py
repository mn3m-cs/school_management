from rest_framework import serializers
from .models import Grade,Class, Student

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['test','student','value']

class ClassSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='name.name')
    class Meta:
        model = Class
        fields = ['name','class_name','day','class_number_in_day']
        

class StudentSerialalizer(serializers.ModelSerializer):
    
    first_name = serializers.CharField(source='user.first_name') # get first_name of user field and use it in fields 
    last_name  = serializers.CharField(source='user.last_name')
    classroom_number = serializers.CharField(source='classroom.class_number')
    level = serializers.CharField(source='classroom.level')
    classroom_pk = serializers.CharField(source='classroom.pk')
    class Meta:
        model = Student
        fields = ['first_name','last_name','classroom_number','level','pk','classroom_pk']