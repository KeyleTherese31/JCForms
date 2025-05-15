from django.contrib.auth.models import AbstractUser
from django.db import models

class AdminUser(AbstractUser):
    email = models.EmailField(unique=True)
