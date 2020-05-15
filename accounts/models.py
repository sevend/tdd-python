from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.

class User(models.Model):
    email = models.EmailField(primary_key=True)
    REQUIRED_FIELDS = ()
    USERNAME_FIELD = 'email'
    is_anonymous = True
    is_authenticated = True

