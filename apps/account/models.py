from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.account.manager import CustomUserManager
from django.utils.translation import gettext_lazy as _



class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

