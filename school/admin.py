from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.School)
admin.site.register(models.Student)
#admin.site.register(models.Teacher)
admin.site.register(models.Classroom)
admin.site.register(models.Course)
#admin.site.register(models.Parents)
admin.site.register(models.Father)
admin.site.register(models.Mother)
admin.site.register(models.Test)
admin.site.register(models.Grade)

class TeacherModelAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(models.Teacher,TeacherModelAdmin)