from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from django.utils import timezone

# Create your models here.

class User(models.Model):
    email = models.EmailField(primary_key=True)
    last_login = models.DateTimeField(default=timezone.now)
    REQUIRED_FIELDS = ()
    USERNAME_FIELD = 'email'
    is_anonymous = True
    is_authenticated = True

