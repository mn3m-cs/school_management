from django.db import models
from django.contrib.auth.models import User


class School(models.Model):
    name = models.CharField(max_length=64)
    classes_number = models.IntegerField(verbose_name="Number of classes")
    teachers_number = models.IntegerField(verbose_name="Number of teachers in all school")
    students_number = models.IntegerField(verbose_name="Number of students in all school") # sum of students in all classes
    location = models.CharField(max_length=280)
    manger = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    ssn = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=264)
    phone =models.IntegerField()
    classrooms = models.ManyToManyField('school.Classroom',related_name='classroom_teachers')
    #specialization = models.ForeignKey('school.Course',on_delete=models.SET_NULL,null=True)
    birth_date = models.DateField(verbose_name='Date of birth')
    #classrooms = models.ForeignKey('school.Classroom',on_delete=models.SET_NULL,related_name='classrooms',null=True)
    photo = models.ImageField(upload_to='teachers/')
    achievements = models.TextField(max_length=1000,null=True,blank=True)
    is_teacher = models.BooleanField(default=True)

    class Meta:
        permissions = (("can_edit_grades","Edit students grades"),)
        ordering = ['name']

    def __str__(self):
        return self.name

class Classroom(models.Model):
    class_number = models.IntegerField(unique=True)
    #classroom_teachers = models.ManyToManyField('school.Teacher',null=True,blank=True)
    levels = [
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
        ('6','6'),
    ]
    level = models.TextField(max_length=2,choices=levels)
    #students = models.ForeignKey('school.Student',on_delete=models.SET_NULL,null=True,related_name='students')
    #to define a many-to-one relationship, use ForeignKey:, we use it in Student Model
    #so we want to retieve students of the class in the classroom_detail view
    class Meta:
        ordering = ['class_number']     
        permissions = (('can_see_classrooms','Can see Classrooms'),)
        
    def __str__(self):
        return str(self.class_number)

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    academic_number = models.IntegerField(unique=True)
    name = models.CharField(max_length=64)
    home_phone = models.IntegerField()
    address = models.CharField(max_length=280)
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE,related_name='students')
    birth_date = models.DateField(verbose_name='Date of birth')
    father = models.ForeignKey('school.Father',on_delete=models.CASCADE,null=True,blank=True)
    mother = models.ForeignKey('school.Mother',on_delete=models.CASCADE,null=True,blank=True)
    photo = models.ImageField(upload_to='students/',blank=True)
    courses = models.ManyToManyField("school.Course",null=True,blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=64)
    picture = models.ImageField(upload_to='courses')
    teacher_of_course = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    classroom = models.ForeignKey("school.classroom",on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    def add_course_to_students_in_class(self):
        students = Student.objects.all()
        classroom = self.classroom
        for student in students:
            if student.classroom == classroom:
                student.courses.add(self)

    def save(self, *args, **kwargs):
        self.add_course_to_students_in_class()
        super(Course, self).save(*args, **kwargs)

class Test(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Grade(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.value)

'''
class Parents(models.Model):
    father = models.ForeignKey('school.Father',on_delete=models.SET_NULL,null=True)
    mother = models.ForeignKey('school.Mother',on_delete=models.SET_NULL,null=True)
    home_phone = models.IntegerField()

    def __str__(self):
        return self.name
'''
class Father(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=64)
    national_id = models.IntegerField(unique=True)
    phone = models.IntegerField()
    job = models.CharField(max_length=150)
    birth_date = models.DateField(verbose_name='Date of birth')

    def __str__(self):
        return self.name

class Mother(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=64)
    national_id = models.IntegerField(unique=True)
    phone = models.IntegerField()
    job = models.CharField(max_length=150)
    birth_date = models.DateField(verbose_name='Date of birth')
    
    def __str__(self):
        return self.name

