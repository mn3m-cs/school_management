from django.urls import path,re_path
from . import views

app_name='school'


urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    path('classrooms/',views.ClassroomsListView.as_view(),name='classrooms'),
    path('classrooms/<int:pk>/',views.ClassroomDetailView.as_view(),name='classroom_detail'),

    path('teachers/',views.TeachersListView.as_view(),name='teachers'),
    path('teachers/<int:pk>/',views.TeacherDetailView.as_view(),name='teacher'),
    
]



