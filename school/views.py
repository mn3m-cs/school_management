from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView,ListView,DetailView
from .models import Classroom,Student,Teacher,Course
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

    return render(request,'school/my_classrooms.html',context={'classrooms':classrooms,
                                                                'teacher':teacher,
                                                                'courses':courses})

class CourseDetailView(UserPassesTestMixin, DetailView):
    def test_func(self):
        return lambda u: u.groups.filter(name='Teacher').exists()
    model = Course
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        ''' return teacher's age '''
        context = {}
        cc = kwargs['object']
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
                course = Course.objects.get(id=cc.id)
                all_students = Student.objects.all()
                students=[]
                for student in all_students:
                    courses = student.courses.all()
                    if course in courses:
                        students.append(student)
        context['students'] = students
        context.update(kwargs)
        return super().get_context_data(**context)
