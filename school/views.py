from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView,CreateView,DeleteView,UpdateView
from django.views.generic.edit import FormView
from .models import Classroom,Student,Teacher,Course,Test,Grade,Class,School,Material,Mother,Father
from datetime import date 
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import TestForm,MettingForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import UplaodCourseMaterialForm
from itertools import chain


class Home(TemplateView):
    template_name = 'school/base.html'
    def get_context_data(self, **kwargs):
        """get school name"""
        context = super().get_context_data(**kwargs)
        school = School.objects.first()
        school_name = school.name
        context['school'] = school_name
        
        return context

#Manager Views#
#----------- Classrooms ---------------#
class ClassroomsListView(UserPassesTestMixin,ListView):
    model = Classroom
    context_object_name = 'classrooms'
    queryset = Classroom.objects.all().order_by('level')

    def test_func(self):
        ''' only admins can see this view'''
        return self.request.user.is_staff
    def get_context_data(self, **kwargs):
        """get school name"""
        context = super().get_context_data(**kwargs)
        school = School.objects.first()
        school_name = school.name
        context['school'] = school_name
        return context

class ClassroomDetailView(UserPassesTestMixin,DetailView):
    model = Classroom
    context_object_name = 'classroom'

    def test_func(self):
        ''' only admins can see this view'''
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        """return students_nubmer in the classroom and get teachers of the classroom"""
        context = super().get_context_data(**kwargs)
        classroom = self.object
        
        #get courses of the classroom
        courses_in_this_classroom = classroom.course_set.all()

        #get teachers of courses in this classroom
        teachers = [course.teacher_of_course for course in courses_in_this_classroom]

        #get classes , operate on courses have classes only, class.name = course.name
        classes=[]
        for course in courses_in_this_classroom:
            for clas in course.course_classes.all():
                classes.append(clas)

        school = School.objects.first()
        school_name = school.name
        context['students_number'] = Student.objects.filter(classroom=self.object.pk).count()
        context['teachers'] = teachers
        context['classes'] = classes
        context['school'] = school_name
        return context

class TeachersListView(ListView):
    model = Teacher
    context_object_name = 'teachers'
    def get_context_data(self, **kwargs):
        """get school name"""
        context = super().get_context_data(**kwargs)
        school = School.objects.first()
        school_name = school.name
        context['school'] = school_name
        return context

class TeacherDetailView(UserPassesTestMixin, DetailView):
    model = Teacher
    context_object_name = 'teacher'
    
    def test_func(self):
        ''' only admins can see this view'''
        return self.request.user.is_staff

    def calculateAge(self,birthDate): 
        today = date.today() 
        age = today.year - birthDate.year -((today.month, today.day) < (birthDate.month, birthDate.day)) 
        return age

    def get_context_data(self, **kwargs):
        ''' return teacher's age '''
        context = {}
        school = School.objects.first()
        school_name = school.name
        context['school'] = school_name
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
                birth_date = self.object.birth_date
                context['age'] = TeacherDetailView.calculateAge(self,birth_date)
        context.update(kwargs)
        return super().get_context_data(**context)

class StudentDetailView(UserPassesTestMixin, DetailView):
    model = Student
    contex_object_name = 'student'

    def calculateAge(self,birthDate): 
        today = date.today() 
        age = today.year - birthDate.year -((today.month, today.day) < (birthDate.month, birthDate.day)) 
        return age

    def get_context_data(self, **kwargs):
        """get school name"""
        context = super().get_context_data(**kwargs)
        school = School.objects.first()
        school_name = school.name
        context['school'] = school_name
        birth_date = self.object.birth_date
        context['age'] = TeacherDetailView.calculateAge(self,birth_date)
        return context
        
    def test_func(self):
        ''' only admins can see this view'''
        return self.request.user.is_staff

class StudentsListView(UserPassesTestMixin,ListView):
    model  = Student
    queryset = Student.objects.all().order_by('classroom')
    context_object_name = 'students'

    def test_func(self):
        ''' only admins can see this view'''
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        """get school name"""
        context = super().get_context_data(**kwargs)
        school = School.objects.first()
        school_name = school.name
        context['school'] = school_name
        return context

class Meeting(FormView):
    form_class = MettingForm
    template_name = 'school/meeting.html'
    success_url = '/school'

    def get_recievers_emails(self,recievers):
        recieversMails = []
        for reciever in recievers:
            recieversMails.append(reciever.user.email)
        print(recieversMails)
        return recieversMails

    def form_valid(self, form):
        cleaned_data = form.clean()
        to = cleaned_data['to'] # 1 = mothres,.....
        subject = cleaned_data['subject']
        body = cleaned_data['body']
        mothers = Mother.objects.all()
        fathers = Father.objects.all()
        mothers_and_fathers = list(chain(mothers, fathers))

        if to == '1':
            recievers = mothers
        elif to =='2':
            recievers = fathers
        elif to =='3':
            recievers = mothers_and_fathers
        elif to =='4':
            recievers = Teacher.objects.all()
        
        self.get_recievers_emails(recievers)
        # send_mail(subject,body,'mohamedabdo581@gmail.com',get_recievers_mails)

        send_mail(subject,body,'mohamedabdo581@gmail.com',('mohamed.ms6@aun.edu.eg',))
        #rTODO: send to recievers but we need mail server
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """get school name"""
        context = super().get_context_data(**kwargs)
        school = School.objects.first()
        school_name = school.name
        context['school'] = school_name
        return context


#---------------- Teacher Views ----------------#

@user_passes_test(lambda u: u.groups.filter(name='Teacher').exists())
def my_courses(request):
    teacher = Teacher.objects.get(user=request.user)
    #classrooms = teacher.classrooms.all()
    all_courses = Course.objects.all()
    courses = []
    for course in all_courses:
        if course.teacher_of_course == teacher:
            courses.append(course)

    school = School.objects.first()
    school_name = school.name
    return render(request,'school/my_courses.html',context={'teacher':teacher,
                                                            'courses':courses,
                                                            'school':school_name})

class CourseDetailView(UserPassesTestMixin, DetailView):
    def test_func(self):
        """
        test if current user is teacher and he is the teacher of this course
        """
        self.object = self.get_object()
        teacher_of_the_course = self.object.teacher_of_course.user
        current_user = self.request.user
        return (self.request.user.groups.filter(name='Teacher').exists() and teacher_of_the_course == current_user) or current_user.is_staff

    model = Course
    context_object_name = 'course'
    form_class = UplaodCourseMaterialForm

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
                    courses = student.classroom.course_set.all()
                    if course in courses:
                        students.append(student)
        context['students'] = students
        context['tests'] = tests
        school = School.objects.first()
        school_name = school.name
        context['school'] = school_name
        #number of students enrolled in this course
        context['students_number'] = self.object.classroom.course_set.all().count()
       #Student.objects.filter(classroom=self.object.classroom).count() --> number of students in classroom of the course
        materials = Material.objects.filter(course=self.get_object())

        context['materials'] = materials
        context.update(kwargs)
        return super().get_context_data(**context)
    
class UploadMaterialFormView(UserPassesTestMixin,FormView):
    form_class = UplaodCourseMaterialForm
    template_name = 'school/upload_material.html'

    def test_func(self):
        '''Here We will test for teacher only, we cant test the current user == teacher_of_course here 
           the form not field yet, this test run before display view, we will test in form_valid
        '''
        return self.request.user.groups.filter(name='Teacher').exists()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UploadMaterialFormView, self).__init__(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(UploadMaterialFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        kwargs = self.get_form_kwargs()
        course = kwargs['data']['course']
        return reverse_lazy('school:course',kwargs={'pk':course})

    def form_valid(self, form):
        kwargs = self.get_form_kwargs()
        course = kwargs['data']['course']
        course_obj = Course.objects.filter(pk=course)[0]
        if self.request.user == course_obj.teacher_of_course.user:
            url = reverse_lazy('school:course',kwargs={'pk':course})
            form.save()
            # return HttpResponseRedirect(url)
            return super().form_valid(form)


    def get_context_data(self, **kwargs):
        """get school name"""
        context = super().get_context_data(**kwargs)
        school = School.objects.first()
        school_name = school.name
        context['school'] = school_name
        return context

class MaterialDeleteView(UserPassesTestMixin,DeleteView):
    model = Material

    def test_func(self):
        return self.request.user == self.get_object().course.teacher_of_course.user

    def get_success_url(self):
        return reverse_lazy('school:course',kwargs={'pk':self.get_object().course.pk})

    def get_context_data(self, **kwargs):
        """get school name"""
        context = super().get_context_data(**kwargs)
        school = School.objects.first()
        school_name = school.name
        context['school'] = school_name
        return context

class TestDetailView(UserPassesTestMixin, DetailView):

    def test_func(self):
        self.object = self.get_object()
        teacher_of_the_course = self.object.course.teacher_of_course.user
        current_user = self.request.user
        return (self.request.user.groups.filter(name='Teacher').exists() and teacher_of_the_course == current_user) or current_user.is_staff

    model = Test
    context_object_name = 'test'

    def get(self, request, *args, **kwargs):
        ''' get course.pk to use it in url'''
        course_num = self.kwargs['pk']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ''' get students enrolled in the course = enrolled in the test
            and their grades '''
        context = super().get_context_data(**kwargs)
        test = self.get_object()
        #to get student and its grade, we can use grades only, because grades contain student data.
        grades_of_test = test.grade_set.all()
        students_grades = {}
        for grade in grades_of_test:
            students_grades[grade.student] = grade

        school = School.objects.first()
        school_name = school.name
        context['school'] = school_name               
        context['enrolled_students'] = students_grades
        context.update(kwargs)
        return context

class TestCreateView(UserPassesTestMixin,CreateView):
    form_class = TestForm
    template_name = 'school/test_form.html'

    def __init__(self, *args, **kwargs):
        '''This for course foreign key, to limit choices to teacher courses only'''
        self.request = kwargs.pop('request', None)
        super(TestCreateView, self).__init__(*args, **kwargs)

    def get_form_kwargs(self):
        '''add user to kwargs of the form, to use it in form'''
        kwargs = super(TestCreateView, self).get_form_kwargs()
        print(kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        '''Test user == teacher_of_course ''' 
        test = form.save(commit=False)
        teacher = test.course.teacher_of_course.user
        current_user = self.request.user
        if teacher == current_user:
            return super().form_valid(form)

    def test_func(self):
        #test if current user is teacher
        current_user = self.request.user
        teacher = Teacher.objects.filter(user=current_user)
        return self.request.user.groups.filter(name='Teacher').exists() 
        

    def get_context_data(self, **kwargs):
        """get school name"""
        context = super().get_context_data(**kwargs)
        school = School.objects.first()
        school_name = school.name
        context['school'] = school_name
        return context

class TestDeleteView(UserPassesTestMixin,DeleteView):
    model = Test
    success_url = reverse_lazy('school:my_courses')

    def test_func(self):
        current_user = self.request.user
        test= self.get_object()
        return current_user == test.course.teacher_of_course.user


    def get_context_data(self, **kwargs):
        """get school name"""
        context = super().get_context_data(**kwargs)
        school = School.objects.first()
        school_name = school.name
        context['school'] = school_name
        return context


#---------------- Student Views ----------------#
class StudentCourses(UserPassesTestMixin,ListView):
    model = Student
    context_object_name = 'courses'
    template_name_suffix = '_student_list'	

    def get_queryset(self):
        student = Student.objects.get(user=self.request.user)
        return student.classroom.course_set.all()

    def get_context_data(self, **kwargs):
        """get school name"""
        context = super().get_context_data(**kwargs)
        school = School.objects.first()
        school_name = school.name
        context['school'] = school_name
        return context

    def test_func(self):
        return self.request.user.groups.filter(name='Student').exists()

class StudentCourseDetailView(UserPassesTestMixin,DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'school/student_course_detail.html'

    def test_func(self):
        #check if student is enrolled in this course <!--TODO: -->
        return self.request.user.groups.filter(name='Student').exists()

    def get_context_data(self, **kwargs):
        """get school name"""
        context = super().get_context_data(**kwargs) # Call the base implementation first to get a context
        school = School.objects.first()
        school_name = school.name
        student = Student.objects.filter(user= self.request.user)[0]
        context['school'] = school_name
        context['student'] =student
        return context

        
#---------------- Parents Views ----------------#
class SonsList(UserPassesTestMixin,ListView):

    context_object_name = 'sons'
    template_name = 'school/sons_list.html'
    
    def test_func(self):
        # Test if user is mother or father 
        return self.request.user.groups.filter(name='Mother') or self.request.user.groups.filter(name='Father')


    def get_queryset(self):
        current_user = self.request.user
        if current_user.groups.filter(name='Father'):
            father = Father.objects.filter(user=current_user)[0]
            queryset = father.student_set.all()

        elif current_user.groups.filter(name='Mother'):
            mother = Mother.objects.filter(user=current_user)[0]
            queryset = mother.student_set.all()    
        
        return queryset

    def get_context_data(self, **kwargs):
        """get school name"""
        context = super().get_context_data(**kwargs)
        school = School.objects.first()
        school_name = school.name
        context['school'] = school_name
        return context

class SonDetailView(UserPassesTestMixin, DetailView):
    model = Student
    context_object_name = 'son'
    template_name = 'school/son_detail.html'

    def calculateAge(self,birthDate): 
        today = date.today() 
        age = today.year - birthDate.year -((today.month, today.day) < (birthDate.month, birthDate.day)) 
        return age

    def test_func(self):
        # Test that the student is son of this user
        student = self.get_object()
        current_user = self.request.user
        if current_user.groups.filter(name='Father'):
            return student.father.user == current_user
        elif current_user.groups.filter(name='Mother'):
            return student.mother.user == current_user

    def get_context_data(self, **kwargs):
        """get school name"""
        context = super().get_context_data(**kwargs)
        school = School.objects.first()
        school_name = school.name
        context['school'] = school_name
        #get tests order by date
        son = self.get_object()
        courses = son.classroom.course_set.all()
        tests = {}

        for course in courses:
            for test in course.test_set.all().order_by('-date'):
                for grade in test.grade_set.all():
                    if grade.student == son:
                        tests[test] = grade

        birth_date = self.object.birth_date
        context['age'] = SonDetailView.calculateAge(self,birth_date)
        context['tests'] = tests
        return context


#### API VIEWS #####
from rest_framework import generics
from .serializers import GradeSerializer,ClassSerializer,StudentSerialalizer
import django_filters.rest_framework
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework import filters
from django.core.mail import send_mail

class IsUserIsCourseTeacher(permissions.BasePermission):
    """
    Custom permission to only allow teachers of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        allowed_methods = ('PUT',)
        if request.method in allowed_methods:
            return obj.test.course.teacher_of_course.user == request.user

class UpdateGrade(generics.UpdateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['test','student']
    lookup_field = 'pk'
    permission_classes = [IsUserIsCourseTeacher]

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

"""
class ViewSchedule(generics.ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['day','class_number_in_day','name']
    permission_classes = [permissions.IsAuthenticated]

    #filter based on classroom
"""

class ViewSchedule(generics.RetrieveAPIView):
    """ we use this instead of listapiview to retirieve courses of every class alone"""
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['day','class_number_in_day','name']
    permission_classes = [permissions.IsAuthenticated]

#search students

class StudentSearch(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerialalizer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['user__first_name','user__last_name']
    ordering = ['classroom',] # default ordering