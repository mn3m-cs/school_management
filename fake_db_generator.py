from faker import Faker
import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE','school_management.settings')

from school.models import Classroom,Course,Mother,Father,Teacher,Student
from random import random

fake = Faker()
levels = [1,2,3,4,5,6]
classrooms = [101,102,103,201,202,203,301,302,303,401,402,403,501,502,503,601,602,603]
fathers = Father.objects.all()
mothers = Mother.objects.all()

def fake_student():
    std = Student.objects.get_or_create(name=fake.name(),
                                        address=fake.address(),
                                        birth_date=fake.date_of_birth(),
                                        level=random.choice(levels)[0],
                                        academic_number=fake.random_init('120111123','120666999'),
                                        home_phone=fake.telephone_number(),
                                        classroom=random.choice(classrooms)[0],
                                        father=random.choice(fathers)[0],
                                        mother=random.choice(mothers)[0],
    )



for i in range(10):
    fake_student()
