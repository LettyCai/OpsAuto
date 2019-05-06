from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.

class UserProfile(AbstractUser):
    job = models.CharField(max_length=100,verbose_name=u'职位',default='')
    mobile = models.CharField(max_length=11,null=True,blank=True)
#    image = models.ImageField(upload_to='image/%Y/%M',default='image/default.png',max_length=100)

    class Meta:
        pass