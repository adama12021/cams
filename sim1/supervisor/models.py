from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

# Create your models here.

class Utilisateur(AbstractUser):
    tel = models.CharField(max_length=20, null=True)
    sex = models.CharField(max_length=3, null=True)
    localites = models.CharField(max_length=200, null=True)
    role = models.CharField(max_length=200,null=True)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
