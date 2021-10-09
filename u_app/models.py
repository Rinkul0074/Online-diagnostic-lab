from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import EmailField
from django.utils import timezone 
from django.contrib.auth import get_user_model 
#from dj_app.models import Test


# Create your models here.

class Userreg(models.Model):
    username = models.CharField(max_length=30)
    emailid = models.CharField(max_length=30)
    phoneno = models.CharField(max_length=30)
    useraddress = models.CharField(max_length=30)
    pincode = models.CharField(max_length=30)
    birthday = models.CharField(max_length=30)
    gender = models.CharField(max_length=30)
    upassword = models.CharField(max_length=30)
    

    def __str__(self):
        return self.username

class Apbook(models.Model):
    usid = models.ForeignKey(Userreg,on_delete=models.CASCADE)
    ustest = models.CharField(default='',max_length=30)
    apdatetime = models.CharField(max_length=30)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ustest + ' -- ' + self.apdatetime



class Transaction(models.Model):
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)