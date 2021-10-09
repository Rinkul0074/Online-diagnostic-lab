from django.shortcuts import render, resolve_url
from django.http.response import HttpResponse
from django.http import request
from u_app.models import Apbook
# from . import Test

from django.conf import settings
from django.core.mail import send_mail
from random import randrange,choices
from .models import *

# Create your views here.

def login(request):
    if request.method == "POST":
        
        password = request.POST['password']
        try:
            uid = User.objects.get(yemail=request.POST['yemail'])
        except:
            msg = 'Email is not registered'
            return render(request,'login.html',{'msg':msg})
        
        if password == uid.password:
            request.session['yemail'] = request.POST['yemail']
            

            return render(request,'dashboard.html',{'uid': uid})
        else:
            msg = 'Password does not matched'
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')



def profile(request):
    uid = User.objects.get(yemail=request.session['yemail'])
    if request.method == 'POST':
        uid.uname=request.POST['uname']
        uid.mnumber=request.POST['mnumber']
        uid.yemail=request.POST['yemail']
        uid.password=request.POST['password']
        if 'pic' in request.FILES:
            uid.pic=request.FILES['pic']
        uid.save()
        msg='update profile sucessfully '
        return render(request,'profile.html',{'uid':uid,'msg':msg})
    else:
        uid = User.objects.get(yemail=request.session['yemail'])
        return render(request,'profile.html')

def register(request):
    if request.method == "POST":
        uname = request.POST['uname']
        mnumber = request.POST['mnumber']
        yemail = request.POST['yemail']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        try:
            uid = User.objects.get(yemail=yemail)
            msg = 'Email Already Register'
            return render(request,'register.html',{'msg':msg})
        except:
            if password == cpassword:
                global temp
                temp = {
                    'uname' : uname,
                    'yemail' : yemail,
                    'mnumber' : mnumber,
                    'password' : password,
                }
                otp = randrange(1000,9999)
                subject = 'welcome to Krishna Lab'
                message = f'Hi your otp for Reset password is {otp}.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [yemail, ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'otp.html',{'otp':otp,'yemail':yemail})


                return render(request,'otp.html',{'otp':otp})
            else:
                msg = 'Password and cpassword not matched'
                return render(request,'register.html',{'msg':msg})

    else:
        return render(request,'register.html')

def otp(request):
    if request.method == "POST":
        otp = request.POST['otp']
        uotp = request.POST['uotp']
        if otp == uotp:
            global temp
            User.objects.create(
                uname = temp['uname'],
                mnumber = temp['mnumber'],
                yemail = temp['yemail'],
                password = temp['password'],
            )
            return render(request,'login.html')
        else:
            msg = 'OTP does not matched'
            return render(request,'otp.html',{'otp':otp,'msg':msg})

    else:
        return render(request,'otp.html')

def logout(request):
    del request.session['yemail']
    return render(request,'dashboard.html')

def forgot1(request):
    if request.method == 'POST':
        yemail = request.POST['yemail']
        try:
            uid = User.objects.get(yemail=yemail)
        except:
            msg = 'Email does not exist'
            return render(request,'forgot pass1.html',{'msg':msg})
        otp = randrange(1000,9999)
        subject = 'welcome to Krishna Lab'
        message = f'Hi your otp for Reset password is {otp}.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [yemail, ]
        send_mail( subject, message, email_from, recipient_list )
        return render(request,'forgot1.html',{'otp':otp,'yemail':yemail})
        

    else:
        return render(request,'forgot pass1.html')

def forgot2(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        uotp = request.POST['uotp']
        yemail = request.POST['yemail']
        if otp == uotp:
            return render(request,'forgot pass3.html',{'yemail':yemail})
        else:
            msg = 'OTP does not matched'
            return render(request,'forgot pass2.html',{'otp':otp,'msg':msg,'yemail':yemail})

    else:

        return render(request,'forgot pass2.html')


def forgot3(request):
    if request.method == 'POST':
        yemail = request.POST['yemail']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            uid = User.objects.get(yemail=yemail)
            uid.password = password
            uid.save()
            return render(request,'login.html')
        else:
            msg = 'Password and Cpassword should be same'
            return render(request,'forgot pass3.html',{'yemail':yemail,'msg':msg})

    else:
        return render(request,'forgot pass3.html')

def addtest(request):
    uid = User.objects.get(yemail=request.session['yemail'])
    if request.method == 'POST':
            Test.objects.create(
                uid = uid,
                ttitle = request.POST['ttitle'],
                tdes = request.POST['tdes'],
                tinter = request.POST['tinter'],
                tprice = request.POST['tprice']
            )
            msg = 'Added test succesfully '
            return render(request,'addtest.html',{'uid':uid,'msg':msg})    
    else:
        return render(request,'addtest.html',{'uid':uid})
    

def managetest(request):
    uid = User.objects.get(yemail=request.session['yemail'])
    tests = Test.objects.all()
    return render(request,'managetest.html',{'tests':tests,'uid':uid})

def delete1(request,pk):
    uid = Test.objects.get(id=pk)
    uid.delete()
    tests = Test.objects.all()
    return render(request,'managetest.html',{'tests':tests})


def new_appointment(request):
    uid = User.objects.get(yemail=request.session['yemail'])
    apubooks = Apbook.objects.all()
    if request.method == 'POST':
        Newuap.objects.create(
            uid=uid,
            apubook= request.POST['sam'],
            bresult = request.POST['bresult'],
            uresult = request.POST['uresult'],
        )
        msg = ('Result Generate sucessfully')
        return render(request,'newap.html',{'uid':uid,'msg':msg} )
    else:
        return render(request,'newap.html',{'apubooks':apubooks})

def report(request):
    uid = User.objects.get(yemail=request.session['yemail'])
    newusap = Newuap.objects.all()
    apubooks = Apbook.objects.all()
    return render(request,'report.html',{'newusap':newusap,'apubooks':apubooks})

def viewreg_user(request):
    uid = User.objects.get(yemail=request.session['yemail'])
    newusap = Newuap.objects.all()
    apubooks = Apbook.objects.all()
    return render(request,'viewreguser.html',{'newusap':newusap,'apubooks':apubooks})


def edittest(request,pk):
    eid = Test.objects.get(id=pk)
    if request.method == "POST":
        eid.ttitle = request.POST['ttitle']
        eid.tdes = request.POST['tdes']
        eid.tinter = request.POST['tinter']
        eid.tprice = request.POST['tprice']
        eid.save()
        uid = User.objects.get(yemail=request.session['yemail'])
        tests = Test.objects.all()
        return render(request,'managetest.html',{'tests':tests,'uid':uid})
    else:
        return render(request,'edittest.html',{'eid':eid})