from django.shortcuts import render
from django.http import request
from django.http.response import HttpResponse
from dj_app.models import Test
from django.views.decorators.csrf import csrf_exempt
from .paytm import *
from django.conf import settings
from .models import Transaction

from django.conf import settings
from django.core.mail import send_mail
from random import randrange,choices
from .models import *
# Create your views here.


def index(request):
    return render(request,'index.html')

def u_register(request):
    if request.method == "POST":
        username = request.POST['username']
        emailid = request.POST['emailid']
        phoneno = request.POST['phoneno']
        useraddress = request.POST['useraddress']
        pincode = request.POST['pincode']
        birthday = request.POST['birthday']
        gender = request.POST['gender']
        upassword = request.POST['upassword']
        ucpassword = request.POST['ucpassword']
        try:
            uid = Userreg.objects.get(emailid=emailid)
            msg = 'Email Already Register'
            return render(request,'u-register.html',{'msg':msg})
        except:
            if upassword == ucpassword:
                global temp1
                temp1 = {
                    'username' : username,
                    'emailid' : emailid,
                    'phoneno' : phoneno,
                    'useraddress' : useraddress,
                    'pincode' : pincode,
                    'birthday' : birthday,
                    'gender' : gender,
                    'upassword' : upassword,
                }
                otp = randrange(1000,9999)
                subject = 'welcome to Krishna Lab'
                message = f'Hi your otp is {otp} , thank you for registering.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [emailid, ]
                send_mail( subject, message, email_from, recipient_list )


                return render(request,'uotp.html',{'otp':otp})
            else:
                msg = 'Password and cpassword not matched'
                return render(request,'u-register.html',{'msg':msg})

    else:
        return render(request,'u-register.html')

def uotp(request):
    if request.method == "POST":
        otp = request.POST['otp']
        uotp = request.POST['uotp']
        if otp == otp:
            global temp1
            Userreg.objects.create(
                username = temp1['username'],
                emailid = temp1['emailid'],
                phoneno = temp1['phoneno'], 
                useraddress = temp1['useraddress'],
                pincode = temp1['pincode'],
                birthday = temp1['birthday'],
                gender = temp1['gender'],
                upassword = temp1['upassword'],

            )
            return render(request,'u-login.html')
        else:
            msg = 'OTP does not matched'
            return render(request,'uotp.html',{'otp':otp,'msg':msg})

    else:
        return render(request,'uotp.html')

def u_login(request):
    if request.method == "POST":
        
        upassword = request.POST['upassword']
        try:
            uid = Userreg.objects.get(emailid=request.POST['emailid'])
        except:
            msg = 'Email is not registered'
            return render(request,'u-login.html',{'msg':msg})
        
        if upassword == uid.upassword:
            request.session['emailid'] = request.POST['emailid']
            

            return render(request,'index.html',{'uid': uid})
        else:
            msg = 'Password does not matched'
            return render(request,'u-login.html',{'msg':msg})
    else:
        return render(request,'u-login.html')

def u_logout(request):
    print(request.session['emailid'])
    del request.session['emailid']
    return render(request,'u-login.html')

def apbook(request):
    usid = Userreg.objects.get(emailid = request.session['emailid'])
    tests = Test.objects.all()
    if request .method == 'POST':
        Apbook.objects.create(
            usid=usid,
            apdatetime = request.POST['apdatetime'],
            ustest = request.POST['plan'],
        )
        msg = ('Appointment book sucessfully')
        return render(request,'apbook.html',{'usid':usid,'msg':msg})
    else: 
        return render(request,'apbook.html',{'tests':tests})


def view_testdetails(request):
    usid = Userreg.objects.get(emailid = request.session['emailid'])
    usid = Userreg.objects.all()
    apubooks = Apbook.objects.all()
    return render(request,'viewtdetails.html',{'apubooks':apubooks,'usid':usid})

def initiate_payment(request):
    if request.method == "GET":
        return render(request, 'payments/pay.html')

    amount = int(request.POST['amount'])


    transaction = Transaction.objects.create(amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str('7465850@gmail.com')),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'payments/redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'payments/callback.html', context=received_data)
        return render(request, 'payments/callback.html', context=received_data)