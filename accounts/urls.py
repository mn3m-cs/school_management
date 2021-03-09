from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from school.models import School

app_name = 'accounts'

urlpatterns=[
    path('login/',LoginView.as_view(template_name='accounts/login.html',
                                    redirect_authenticated_user=True,
                                    extra_context={'school':School.objects.first()})
    ,name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    

]