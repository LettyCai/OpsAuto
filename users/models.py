from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.

class UserProfile(AbstractUser):
    role_choices = {
        (0,"系统管理员"),
        (1,"运维人员"),
        (2,"值班人员"),
    }
    role = models.IntegerField(choices=role_choices,default=2)
    job = models.CharField(max_length=100,verbose_name=u'职位',default='')
    mobile = models.CharField(max_length=11,null=True,blank=True)
#    image = models.ImageField(upload_to='image/%Y/%M',default='image/default.png',max_length=100)


    class Meta:
        pass