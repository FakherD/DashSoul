from django.db import models
from django.contrib.auth.models import AbstractUser
#from django_countries.fields import CountryField
#from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Profile(AbstractUser):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    emailaddress =models.CharField(max_length=100, unique= True)
    password = models.CharField(max_length=100)
    username= None
    USERNAME_FIELD = 'emailaddress'


   # country = CountryField(default='US')
   # phone_number = PhoneNumberField()


