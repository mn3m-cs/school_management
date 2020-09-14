from django.urls import path,re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name='school'


urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    path('classrooms/',views.ClassroomsListView.as_view(),name='classrooms'),
    path('classrooms/<int:pk>/',views.ClassroomDetailView.as_view(),name='classroom_detail'),

    path('teachers/',views.TeachersListView.as_view(),name='teachers'),
    path('teachers/<int:pk>/',views.TeacherDetailView.as_view(),name='teacher'),

    path('students/<int:pk>/',views.StudentDetailView.as_view(),name='student_detail'),
    
    path('edit/',views.TestPerm.as_view(),name='tst'),
    
    path('my_courses/',views.my_classrooms,name='my_courses'),
    path('course/<int:pk>/',views.CourseDetailView.as_view(),name='course'),
    
    path('course/<int:course_num>/test/<int:pk>/',views.TestDetailView.as_view(),name='test_detail'),
    
    #API
    path('grade_api/',views.Grades.as_view(), name='grade_api'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
