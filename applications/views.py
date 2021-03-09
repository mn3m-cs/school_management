from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import StudentApplicationForm
from school.models import School


class StudentApplicationFormView(SuccessMessageMixin,FormView):
    form_class = StudentApplicationForm
    template_name = 'applications/student_application.html'
    success_url = '/school'
    success_message = 'Thanks, We have recieved your applications, we will contact you when enrollments starts.'

    def get_context_data(self, **kwargs):
        """get school name"""
        context = super().get_context_data(**kwargs)
        school = School.objects.first()
        school_name = school.name
        context['school'] = school_name
        return context

    def form_valid(self, form):
        form.save()
        return super(StudentApplicationFormView, self).form_valid(form)
