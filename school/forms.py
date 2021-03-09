from django import forms
from school.models import Test,Course,Teacher,Material,Meeting

class TestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = ['course','name','date','duration','mark']
        
    def __init__(self, *args, **kwargs):
       user = kwargs.pop('user')
       super(TestForm, self).__init__(*args, **kwargs)
       teacher = Teacher.objects.get(user=user)
       self.fields['course'].queryset = Course.objects.filter(teacher_of_course=teacher)
       
    
class UplaodCourseMaterialForm(forms.ModelForm):
    
    class Meta:
        model = Material
        fields = ('course','material_file','title')
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(UplaodCourseMaterialForm,self).__init__(*args, **kwargs)
        teacher = Teacher.objects.get(user=user)
        self.fields['course'].queryset = Course.objects.filter(teacher_of_course=teacher)

class MettingForm(forms.ModelForm):
    
    class Meta:
        model = Meeting
        fields= ['to','subject','body']

        widgets = { 
            'body': forms.Textarea(),
            }