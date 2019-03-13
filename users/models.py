from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.

class UserProfile(AbstractUser):
    nick_user = models.CharField(max_length=50,verbose_name=u"昵称",default="")
    gender = models.CharField(max_length=8,choices=(('male',u'男'),('female',u'女')),default='female')
    job = models.CharField(max_length=100,verbose_name=u'职位',default='')
    mobile = models.CharField(max_length=11,null=True,blank=True)
#    image = models.ImageField(upload_to='image/%Y/%M',default='image/default.png',max_length=100)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

        def __str__(self):
            return self.username