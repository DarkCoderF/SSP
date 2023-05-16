from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class UserInfo(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True)
    about = models.TextField(blank=True)
    photo = models.ImageField(blank=True,upload_to='uploads/user')

    def __str__(self):
        return "user {}".format(self.user.username)
