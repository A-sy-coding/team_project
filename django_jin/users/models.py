from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
class Profile(AbstractUser):
    name = models.CharField(max_length=200)

class auth_number(models.Model):
    
    auth_number = models.IntegerField()