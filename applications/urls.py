from django.urls import path
from . import views



app_name = 'applications'

urlpatterns = [
    path('student_application/',views.StudentApplicationFormView.as_view(),name='apply'),
    
]
