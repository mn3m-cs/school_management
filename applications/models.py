from django.db import models


GENDER_CHOICES = (
    (0, 'Male'),
    (1, 'Female'),)

class StudentApplication(models.Model):
    name = models.CharField(max_length=100,verbose_name='Full Name')
    home_phone = models.CharField(max_length=20)
    birth_date = models.DateField(verbose_name='Date of Birth')
    gender = models.IntegerField(choices=GENDER_CHOICES)

    street = models.CharField(max_length=150,)
    city = models.CharField(max_length=20)
    
    #الوصي
    email = models.EmailField()
    contact_1_name = models.CharField(max_length=50,verbose_name='Contact 1 Name')
    contact_1_phone = models.CharField(max_length=20,verbose_name='Contact 1 Phone')

    contact_2_name = models.CharField(max_length=50,verbose_name='Contact 2 Name')
    contact_2_phone = models.CharField(max_length=20,verbose_name='Contact 1 Phone')

    def __str__(self):
        return self.name

    