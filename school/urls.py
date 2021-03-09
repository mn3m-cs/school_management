from django.urls import path,re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name='school'


urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    path('classrooms/',views.ClassroomsListView.as_view(),name='classrooms'),
    path('classrooms/<int:pk>/',views.ClassroomDetailView.as_view(),name='classroom_detail'),

    path('students/',views.StudentsListView.as_view(),name='students'),
    path('teachers/',views.TeachersListView.as_view(),name='teachers'),
    path('teachers/<int:pk>/',views.TeacherDetailView.as_view(),name='teacher'),
    path('test/',views.TestCreateView.as_view(),name='create_test'),
    path('test/delete/<int:pk>/',views.TestDeleteView.as_view(),name='delete_test'),
    path('students/<int:pk>/',views.StudentDetailView.as_view(),name='student_detail'),

    path('teacher-courses/',views.my_courses,name='my_courses'),  
    path('course/<int:pk>/',views.CourseDetailView.as_view(),name='course'),
    path('course/<int:course_num>/test/<int:pk>/',views.TestDetailView.as_view(),name='test_detail'),
    path('upload-material/',views.UploadMaterialFormView.as_view(),name='upload_material'),
    path('delete-material/<int:pk>/',views.MaterialDeleteView.as_view(),name='delete_material'),

    path('meetings/',views.Meeting.as_view(),name='meetings'),

    #Parents
    path('sons/',views.SonsList.as_view(),name='sons_list'),
    path('sons/<int:pk>/',views.SonDetailView.as_view(),name='son_detail'),
    
    #student
    path('student-courses/',views.StudentCourses.as_view(),name='student_courses'), #rTODO: <student>/
    path('student-courses/<int:pk>/',views.StudentCourseDetailView.as_view(),name='student_course_detail'),






    #API
    #path('grade_api/',views.Grades.as_view(), name='grade_api'),
    path('update_grade_api/<int:pk>/',views.UpdateGrade.as_view(), name='update_grade'),
    path('view_schedule/<int:pk>/',views.ViewSchedule.as_view(), name='view_schedule'),
    path('search_student/',views.StudentSearch.as_view(),name='search_student'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
