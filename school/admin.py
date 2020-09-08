from django.contrib import admin
from . import models

admin.site.register(models.School)
admin.site.register(models.Student)
admin.site.register(models.Teacher)
admin.site.register(models.Classroom)
#admin.site.register(models.Course)
#admin.site.register(models.Test)
admin.site.register(models.Grade)
#admin.site.register(models.Parents)
admin.site.register(models.Father)
admin.site.register(models.Mother)


'''
class TeacherModelAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(models.Teacher,TeacherModelAdmin)
'''

class TestInline(admin.StackedInline):
    model = models.Test

class StudentInline(admin.TabularInline):
    model= models.Student
    def get_queryset(request):
        return Student.objects.filter(classroom=self.object.pk)


class GradesInline(admin.TabularInline):
    model = models.Grade

class CourseAdmin(admin.ModelAdmin):
    inlines = [TestInline]
admin.site.register(models.Course, CourseAdmin)


class TestAdmin(admin.ModelAdmin):
    inlines = [GradesInline]
admin.site.register(models.Test, TestAdmin)
