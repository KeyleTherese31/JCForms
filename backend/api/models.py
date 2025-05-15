from django.contrib.auth.models import AbstractUser
from django.db import models

class AdminUser(AbstractUser):
    # You can add custom fields if needed
    class Meta:
        verbose_name = 'admin user'
        verbose_name_plural = 'admin users'
