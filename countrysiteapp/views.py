import http
import http.client
import random
import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import login
from countrysiteapp.Forms import  loginForm
from django.contrib.auth import authenticate,logout
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request,'index.html')

def login(request):
    if request.method=='POST':
        form = loginForm(request.POST)
        if form.is_valid():
            x = otp_send(request)
            if x:
                return render(request, 'otp_input.html')
            else:
                return render(request, 'login.html')

        else:
            form=loginForm
            return render(request,login.html,{'form':form})
    else:
        form = loginForm
        return render(request,'login.html',{'form':form})

def otpvalidation(request):
    newotp = request.POST['otp']
    oldotp = request.session['otp']
    if newotp == oldotp:
        form = loginForm(request.session["details"])
        form.save()
      # login is a function
        return render(request, 'welcome.html')
    else:
        return render(request, 'otp_input.html')

def otp_send(request):
    ot = str(random.randint(100000, 999999))
        # request.session["pwd"]=request.POST["t1"]
    phone = request.POST["phone"]
        # temail=request.POST["email"]
        # request.session["un"] = request.POST["email"]
        # request.session["pw"] = request.POST["Password"]
        # subject = "registration otp"
        # From_mail=settings.EMAIL_HOST_USER
        # to_list=[temail]
        # send_mail(subject, ot, From_mail, to_list, fail_silently=False)
    print("otp sent to email")
    request.session["details"] = request.POST
    request.session["otp"] = ot
    conn = http.client.HTTPSConnection("api.msg91.com")

    payload = "{ \"sender\": \"KARTHK\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": \"" + ot + "\", \"to\": [ \"" + phone + "\" ]}]}"

    headers = {
            'authkey': "295863A5LW905fm05d8b401e",
            'content-type': "application/json"
        }

    conn.request("POST", "/api/v2/sendsms?country=91", payload, headers)

        # res = conn.getresponse()
        # data = res.read()

        # k=data.decode("utf-8")
    data = conn.getresponse()
    res = json.loads(data.read().decode("UTF-8"))
    print(res)

    if res["type"] == "success":
        return True
    else:
        return False

@login_required
# def login(request):
#     return render(request, "includes/welcome.html")

def my_logout(request):
    logout(request)
    return render(request, 'index.html')
