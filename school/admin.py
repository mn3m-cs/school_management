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
admin.site.register(models.Specialization)
admin.site.register(models.Class)
admin.site.register(models.Material)
admin.site.register(models.Meeting)


'''
class TeacherModelAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(models.Teacher,TeacherModelAdmin)
'''

class TestInline(admin.StackedInline):
    model = models.Test
    
class CourseAdmin(admin.ModelAdmin):
    inlines = [TestInline]
admin.site.register(models.Course, CourseAdmin)

class GradesInline(admin.TabularInline):
    model = models.Grade
class TestAdmin(admin.ModelAdmin):
    inlines = [GradesInline]
admin.site.register(models.Test, TestAdmin)