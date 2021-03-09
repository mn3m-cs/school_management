from django import forms
from .models import StudentApplication


class StudentApplicationForm(forms.ModelForm):

    class Meta:
        model = StudentApplication
        fields = ['name','home_phone','birth_date','gender',
        'street','city',
        'email',
        'contact_1_name','contact_1_phone',
        'contact_2_name','contact_2_phone',
        ]