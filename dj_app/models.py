from django.db import models
from django.db.models.fields import EmailField
from django.utils import timezone  
from u_app.models import *
# Create your models here.

class User(models.Model):

    uname = models.CharField(max_length=30)
    mnumber = models.CharField(max_length=30)
    yemail = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    pic = models.FileField(upload_to='profile/',null=True,blank=True)

    def __str__(self):
        return self.uname


class Test(models.Model):
    uid = models.ForeignKey(User,on_delete=models.CASCADE)
    ttitle = models.CharField(max_length=20)
    tdes = models.CharField(max_length=100)
    tinter = models.CharField(max_length=100)
    tprice = models.CharField(max_length=20)

    def __str__(self):
        return self.ttitle

class Newuap(models.Model):
    uid = models.ForeignKey(User,on_delete=models.CASCADE)
    apubook = models.CharField(default='',max_length=20)
    bresult = models.CharField(max_length=20)
    uresult = models.CharField(max_length=30)

    def __str__(self):
        return self.bresult + ' ' + self.uresult + ' ' + self.apubook