import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_management.settings")

import django
django.setup()
from django.core.management import call_command
from faker import  Faker
from school.models import *
fake = Faker()
import random

def fake_groups():
    groups = ['Student','Teacher','Mother','Father']
    for g in groups:
        Group.objects.get_or_create(name=g)

def fake_classrooms(num):
    for i in range(num):
        n = fake.unique.random_number(3)
        level = fake.random.randint(1,6)
        Classroom.objects.get_or_create(class_number = n,
        level=level,
        )

def fake_mother(num):
    for i in range(num):
        user = User.objects.create(username = fake.unique.user_name())
        national_ID = fake.unique.random_number(14)
        birth_date = fake.date_of_birth()
        phone = fake.random_number(8)
        job = fake.job()
        Mother.objects.create(user=user,
        national_ID = national_ID,
        phone = phone,
        job = job,
        birth_date=birth_date
        )
        u = User.objects.get(username=user)
        u.first_name = fake.first_name()
        u.last_name  = fake.last_name()
        u.save()

def fake_father(num):
    for i in range(num):
        user = User.objects.create(username = fake.unique.user_name())
        national_ID = fake.unique.random_number(14)
        birth_date = fake.date_of_birth()
        phone = fake.random_number(8)
        job = fake.job()
        Father.objects.create(user=user,
        national_ID = national_ID,
        phone = phone,
        job = job,
        birth_date=birth_date
        )
        u = User.objects.get(username=user)
        u.first_name = fake.first_name()
        u.last_name  = fake.last_name()
        u.save()

def fake_studends(num):
    # fake user then use it 
    for i in range(num):
        user = User.objects.create(username = fake.unique.user_name())
        national_ID = fake.unique.random_number(14)
        academic_number = fake.unique.random_number(9)
        address = fake.unique.address()
        classrooms  = Classroom.objects.all()
        classroom = classrooms[random.randint(1,len(classrooms)-1)]
        birth_date = fake.date_of_birth()
        fathers = Father.objects.all()
        father = fathers[random.randint(1,len(fathers)-1)]
        mothers = Mother.objects.all()
        mother = mothers[random.randint(1,len(mothers)-1)]
        gender = random.randint(0,1)
        home_phone = fake.random_number(8)
        Student.objects.create(user=user, national_ID=national_ID,
        academic_number = academic_number,
        address=address,
        classroom=classroom,
        birth_date=birth_date,
        father=father,
        mother=mother,
        gender=gender,
        home_phone=home_phone,
        )
        u = User.objects.get(username=user)
        u.first_name = fake.first_name()
        u.last_name  = fake.last_name()
        u.save()

def fake_teacher(num):
    for i in range(num):
        user = User.objects.create(username = fake.unique.user_name())
        national_ID = fake.unique.random_number(14)
        address = fake.unique.address()
        birth_date = fake.date_of_birth()
        gender = random.randint(0,1)
        phone = fake.random_number(8)
        specializations = Specialization.objects.all()
        sp = specializations[random.randint(1,len(specializations)-1)]
        Teacher.objects.create(user=user, national_ID=national_ID,
        address=address,
        birth_date=birth_date,
        gender=gender,
        phone=phone,
        specialization=sp,
        )
        u = User.objects.get(username=user)
        u.first_name = fake.first_name()
        u.last_name  = fake.last_name()
        u.save()

def fake_school():
    School.objects.create(name='Dar Hagr School',
    classrooms_number = 100,
    teachers_number = 780,
    students_number = 2000,
    location = 'Assiut - Mucha'
    ,manger = 'Mohamed Ali Hanafy'
    )

def fake_sepcialization(num):
    ss = ['Arabic Language', 'Arabic Font', 
        'History','Geography','Geology','Zology','Sciences','Math'
        ,'English','Spanish','Islamic Religion',
        ]

    for i in range(num):
        name = ss[random.randint(1,len(ss)-1)]
        Specialization.objects.create(name=name)

def fake_courses(num):
    ss = ['Arabic Language', 'Arabic Font', 
        'History','Geography','Geology','Zology','Sciences','Math'
        ,'English','Spanish','Islamic Religion',
        ]
    for i in range(num):
        name = ss[random.randint(1,len(ss)-1)]
        code = fake.random_number(3)
        teachers = Teacher.objects.all()
        teacher = teachers[random.randint(1,len(ss)-1)]
        classrooms  = Classroom.objects.all()
        classroom = classrooms[random.randint(1,len(classrooms)-1)]
        Course.objects.create(code=code,name=name,teacher_of_course=teacher,
        classroom=classroom
        )

#rTODO: fake_grades()
#rTODO: fake_tests()

# fake_school()
# fake_groups()
# fake_classrooms(5)
# fake_mother(5)
# fake_father(5)
# fake_sepcialization(5)
fake_studends(400)
# fake_teacher(5)
# fake_courses(15)
