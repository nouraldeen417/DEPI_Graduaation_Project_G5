from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail

class Device(models.Model):
    uniqename = models.CharField (max_length=100,  unique=True)
    hostname  = models.CharField (max_length=100,  unique=True)
    ip        = models.CharField (max_length=15 ,  unique=True)

    def __str__(self):
        return self.uniqename
    