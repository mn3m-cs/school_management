from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView,ListView,DetailView
from .models import Classroom,Student,Teacher,Course,Test,Grade
from datetime import date 
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin


class Home(TemplateView):
    template_name = 'school/base.html'

#Manager Views#
#-----------Classrooms ---------------#
class ClassroomsListView(ListView):
    model = Classroom
    context_object_name = 'classrooms'
    
    
class ClassroomDetailView(DetailView):
    model = Classroom
    context_object_name = 'classroom'

    def get_context_data(self, **kwargs):
        """return students_nubmer in the classroom"""
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context['students_number'] = Student.objects.filter(classroom=self.object.pk).count()
        context.update(kwargs)
        return super().get_context_data(**context)

class TeachersListView(ListView):
    model = Teacher
    context_object_name = 'teachers'

class TeacherDetailView(DetailView):
    model = Teacher
    context_object_name = 'teacher'
    
    def calculateAge(self,birthDate): 
        today = date.today() 
        age = today.year - birthDate.year -((today.month, today.day) < (birthDate.month, birthDate.day)) 
        return age

    def get_context_data(self, **kwargs):
        ''' return teacher's age '''
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
                birth_date = self.object.birth_date
                context['age'] = TeacherDetailView.calculateAge(self,birth_date)
        context.update(kwargs)
        return super().get_context_data(**context)

class StudentDetailView(DetailView):
    model = Student
    contex_object_name = 'student'
    
class TestPerm(PermissionRequiredMixin, TemplateView):
    permission_required = ('school.can_edit_grades')
    PermissionError('Teachers only can edit grades.')
    template_name = 'school/hi.html'




#----------------Teacher Views ----------------#

@user_passes_test(lambda u: u.groups.filter(name='Teacher').exists())
def my_classrooms(request):
    teacher = Teacher.objects.get(user=request.user)
    classrooms = teacher.classrooms.all()
    all_courses = Course.objects.all()
    courses = []
    for course in all_courses:
        if course.teacher_of_course == teacher:
            courses.append(course)

    return render(request,'school/my_courses.html',context={'classrooms':classrooms,
                                                                'teacher':teacher,
                                                                'courses':courses})

class CourseDetailView(UserPassesTestMixin, DetailView):
    def test_func(self):
        """
        test if current user is teacher and he is the teacher of this course
        """
        self.object = self.get_object()
        teacher_of_the_course = self.object.teacher_of_course.user
        current_user = self.request.user
        return self.request.user.groups.filter(name='Teacher').exists() and teacher_of_the_course == current_user

    model = Course
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        ''' return  '''
        context = {}
        cc = kwargs['object']
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
                course = Course.objects.get(id=cc.id)
                tests = course.test_set.all()
                all_students = Student.objects.all()
                students=[]
                for student in all_students:
                    courses = student.courses.all()
                    if course in courses:
                        students.append(student)
        context['students'] = students
        context['tests'] = tests
        context.update(kwargs)
        return super().get_context_data(**context)


class TestDetailView(UserPassesTestMixin, DetailView):
    def test_func(self):
        self.object = self.get_object()
        teacher_of_the_course = self.object.course.teacher_of_course.user
        current_user = self.request.user
        return self.request.user.groups.filter(name='Teacher').exists() and teacher_of_the_course == current_user

    model = Test
    context_object_name = 'test'

    def get(self, request, *args, **kwargs):
        ''' get course.pk to use it in url'''
        course_num = self.kwargs['pk']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ''' get students enrolled in the course = enrolled in the test
            and their grades '''
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
                all_students = Student.objects.all()
                test = self.object
                course = self.object.course
                students = []
                students_grades = {}
        
                all_grades = Grade.objects.all()
                for student in all_students:
                    for grade in all_grades:
                        if course in student.courses.all() and grade.student == student and grade.test == test:
                                students_grades[student] = grade
                        
        context['enrolled_students'] = students_grades
        context.update(kwargs)
        return super().get_context_data(**context)



###### REST API VIEWS ######
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Grade
from .serializers import GradeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins

@api_view(['GET','POST'])
def grades_list(requset , format=None):
    if requset.method == "GET":
        grades = Grade.objects.all()
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

    elif requset.method == "POST":
        serializer = GradeSerializer(data=requset.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def grade_detail(request, pk , format=None):

    try:
        grade = Grade.objects.get(pk=pk)
    except Grade.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GradeSerializer(grade)
        print
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = GradeSerializer(grade, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        grade.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

from rest_framework import generics

class StudentGrade(generics.ListAPIView):
    serializer_class = GradeSerializer

    def get_queryset(self):

        queryset = Grade.objects.all()
        student = self.request.query_params.get('student', None)
        test = self.request.query_params.get('test', None)
        
        if student is not None:
            queryset = queryset.filter(student = student , test = test )
            return queryset

    