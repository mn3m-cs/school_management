from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import Group

GENDER_CHOICES = (
    (0, 'Male'),
    (1, 'Female'),)

class School(models.Model):
    name = models.CharField(max_length=64)
    classrooms_number = models.IntegerField(verbose_name="Number of classes",blank=True,null=True)
    teachers_number = models.IntegerField(verbose_name="Number of teachers in all school",blank=True,null=True)
    students_number = models.IntegerField(verbose_name="Number of students in all school",blank=True,null=True) # sum of students in all classes
    location = models.CharField(max_length=280)
    manager = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    national_ID = models.IntegerField(unique=True,blank=True,null=True)
    address = models.CharField(max_length=264)
    phone =models.IntegerField()
    specialization = models.ForeignKey('school.Specialization',on_delete=models.CASCADE,null=True)
    birth_date = models.DateField(verbose_name='Date of birth')
    photo = models.ImageField(upload_to='teachers/',blank=True,null=True)
    achievements = models.TextField(max_length=1000,null=True,blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES)

    def __str__(self):
        name = '{} {}'.format(self.user.first_name,self.user.last_name)
        return name

    def save(self, *args, **kwargs):
        # add this user to "Teacher" group
        model_group = Group.objects.filter(name='Teacher')[0]

        # if user no a member of any groups
        if self.user.groups.count() == 0 :
            model_group.user_set.add(self.user)
            super(Teacher, self).save(*args, **kwargs)
        
        # if user in this group . Used on "update"
        elif self.user.groups.all()[0] == model_group:
            super(Teacher, self).save(*args, **kwargs)
            
        else:
            user_group = self.user.groups.all()[0]
            raise ValidationError('This user in a {} group'.format(user_group))

class Specialization(models.Model):
    name = models.CharField(max_length=64)
    picture = models.ImageField(upload_to='specializations/',null=True,blank=True)

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
    #courses = models.ManyToManyField("school.Course", null=True,blank=True)

    #students = models.ForeignKey('school.Student',on_delete=models.SET_NULL,null=True,related_name='students')
    #to define a many-to-one relationship, use ForeignKey:, we use it in Student Model
    #so we want to retieve students of the class in the classroom_detail view
    class Meta:
        ordering = ['class_number']     
        #permissions = (('can_see_classrooms','Can see Classrooms'),)
        
    def __str__(self):
        return str(self.class_number)

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    national_ID = models.IntegerField(unique=True,blank=True,null=True)
    academic_number = models.IntegerField(unique=True)
    #name = models.CharField(max_length=64)
    home_phone = models.IntegerField(blank=True,null=True)
    address = models.CharField(max_length=280)
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE,related_name='students')
    birth_date = models.DateField(verbose_name='Date of birth')
    father = models.ForeignKey('school.Father',on_delete=models.CASCADE,null=True,blank=True)
    mother = models.ForeignKey('school.Mother',on_delete=models.CASCADE,null=True,blank=True)
    photo = models.ImageField(upload_to='students/',blank=True,null=True)
    # courses = models.ManyToManyField("school.Course", null=True,blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES)


    # class Meta:
        # ordering = ['name']

    def __str__(self):
        name = '{} {}'.format(self.user.first_name,self.user.last_name)
        return name

    def save(self, *args, **kwargs):
        # add courses in the classroom which student is added to, to this student. 
        # classroom_courses = self.courses.all()
        # print(classroom_courses)



        # add this user to "Student" group
        model_group = Group.objects.filter(name='Student')[0]
        # if user no a member of any groups
        if self.user.groups.count() == 0 :
            model_group.user_set.add(self.user)
            super(Student, self).save(*args, **kwargs)
        # if user in this group . Used on "update"
        elif self.user.groups.all()[0] == model_group:
            super(Student, self).save(*args, **kwargs)
            
        else:
            user_group = self.user.groups.all()[0]
            raise ValidationError('This user in a {} group'.format(user_group))

class Course(models.Model):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=64)
    teacher_of_course = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    classroom = models.ForeignKey("school.classroom",on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    # def add_course_to_students_in_class(self):
    #     students = Student.objects.all()
    #     classroom = self.classroom
    #     for student in students:
    #         if student.classroom == classroom:
    #             student.courses.add(self)


    def save(self, *args, **kwargs):
    #     ''' we need to save course before add m2m relation'''
    #     super(Course, self).save(*args, **kwargs)
    #     self.add_course_to_students_in_class()

        if self in Course.objects.all():
            n= self.name.split('_')[0]
            self.name = n +'_{}'.format(str(self.classroom))
        else:
            self.name += '_{}'.format(str(self.classroom))

        super(Course, self).save(*args, **kwargs)
        
class Test(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(help_text ='Format: <b>Year:Month:Day Hour:Minute</b> <i>example: 2021-2-26 10:00</i>')
    duration = models.SmallIntegerField()
    mark = models.SmallIntegerField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        '''edit save method to initiate grade object for every student when test is created'''
        # get students in the classroom of the course
        students = self.course.classroom.students.all()
        for student in students:
            # if self.course in student.classroom.course_set.all():
            super(Test, self).save(*args, **kwargs)
            grade = Grade.objects.get_or_create(test=self,student=student)

    def get_absolute_url(self):
        return reverse('school:test_detail',kwargs={'course_num':self.course.pk,'pk':self.pk})

class Grade(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(blank=True,null=True)
    #uniqe_together = ['test','student']

    def __str__(self):
        return str(self.value)

    def save(self, *args, **kwargs):
        # If Student not enrolled in this course
        if self.test.course in self.student.classroom.course_set.all():
            # IF grade <= Full Mark
            if self.value is not None:
                if self.value <= self.test.mark:
                    ''' if student have grade in this test, update grade '''
                    grades = Grade.objects.filter(student=self.student,test=self.test)
                    if grades:
                        grades = Grade.objects.filter(student=self.student,test=self.test).update(value=self.value)
                    else:
                        super(Grade, self).save(*args, **kwargs)
                else:
                    self.value = self.test.mark
                    super(Grade, self).save(*args, **kwargs)
                    #raise ValidationError('Mark cannot be larger than the full Mark, so mark will be equal to full mark')
            else:
                super(Grade, self).save(*args, **kwargs)

class Father(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    #name = models.CharField(max_length=64)
    national_ID = models.IntegerField(unique=True,blank=True,null=True)
    phone = models.IntegerField()
    job = models.CharField(max_length=150)
    birth_date = models.DateField(verbose_name='Date of birth')

    def __str__(self):
        name = '{} {}'.format(self.user.first_name,self.user.last_name)
        return name


    def save(self, *args, **kwargs):
        # add this user to "Father" group
        model_group = Group.objects.filter(name='Father')[0]

        
        # if user no a member of any groups
        if self.user.groups.count() == 0 :
            model_group.user_set.add(self.user)
            super(Father, self).save(*args, **kwargs)
        
        # if user in this group . Used on "update"
        elif self.user.groups.all()[0] == model_group:
            super(Father, self).save(*args, **kwargs)
    
        else:
            user_group = self.user.groups.all()[0]
            raise ValidationError('This user in a {} group'.format(user_group))

class Mother(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    #name = models.CharField(max_length=64)
    national_ID = models.IntegerField(unique=True,blank=True,null=True)
    phone = models.IntegerField()
    job = models.CharField(max_length=150)
    birth_date = models.DateField(verbose_name='Date of birth')
    
    def __str__(self):
        name = '{} {}'.format(self.user.first_name,self.user.last_name)
        return name


    def save(self, *args, **kwargs):
        # add this user to "Mother" group
        model_group = Group.objects.filter(name='Mother')[0]

        # if user no a member of any groups
        if self.user.groups.count() == 0 :
            model_group.user_set.add(self.user)
            super(Mother, self).save(*args, **kwargs)

        # if user in this group . Used on "update"
        elif self.user.groups.all()[0] == model_group:
            super(Mother, self).save(*args, **kwargs)
            
        else:
            user_group = self.user.groups.all()[0]
            raise ValidationError('This user in a {} group'.format(user_group))

class Class(models.Model):
    days=[
        ('0', 'saturday'),
        ('1', 'sunday'),
        ('2','monday'),
        ('3', 'tuesday'),
        ('4','wednesday'),
        ('5','thursday'),
        ('6','friday'),
    ]
    name = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='course_classes') #course contain classroom data
    day = models.CharField(max_length=1,choices=days)
    class_number_in_day = models.IntegerField()
    class Meta:
        ordering = ['day']
        verbose_name_plural ='Classes'

    def __str__(self):
        return str(self.name.name)

class Material(models.Model):
    course = models.ForeignKey('school.course', on_delete=models.CASCADE)
    material_file = models.FileField(verbose_name='File',upload_to='materials/')
    title = models.CharField(max_length=50)

    def __str__(self):
        t = '{} - {}'.format(self.title,self.course)
        return str(t)

class Meeting(models.Model):
    choices = [('1','Mothers'),
                ('2','Fathers'),
                ('3','Fathers and Mothers'),
                ('4','Teachers')
                ]
    to = models.CharField(max_length=20,choices=choices,verbose_name='To')
    subject = models.CharField(max_length=50,verbose_name='Subject')
    body = models.CharField(max_length= 3000 ,verbose_name = 'Body')

    def __str__(self):
        return self.subject