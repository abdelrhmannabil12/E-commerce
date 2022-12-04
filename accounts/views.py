from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages,auth
from .forms import RegisterationForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.
def register(request):
    if request.method == 'POST':
        form=RegisterationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=email.split('@')[0]
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.save()


            current_site=get_current_site(request)
            mail_subject="Please Active Your account"
            message=render_to_string('verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email 
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Registeration Successful')
            return redirect('register')
    else:
        form=RegisterationForm()
    return render(request,'register.html',{"form":form})



def login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']

        user= auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"You Are Now Looged In")
            return redirect('dashboard')
        else:
            messages.error(request,"wrong password or username , please try again")
            return redirect('login')
    return render(request,'login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,"You are Logged out")
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"Congratulations! your account is activated")
        return redirect('login')
    else:
        messages.error(request,"Invalid Activation Link")
        return redirect('register')


@login_required(login_url='login')
def dashboard(request):
    return render(request,'dashboard.html')


def forgotpassword(request):
    if request.method == 'POST':
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)
            current_site=get_current_site(request)
            mail_subject="Put New Password"
            message=render_to_string('reset_password.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email 
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Check your mail')
            return redirect('login')
        else:
            messages.error(request,'Account does Not Exist')
            return redirect('forgotpassword')
    return render(request,'forgotpassword.html')

def resetpassword(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Please reset your password')
        return redirect('reset')
    else:
        messages.error(request,'This Link has been expired!')
        return redirect('login')


def reset(request):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirmpassword']

        if password==confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password has been changed')
            return redirect('login')
        else:
            messages.error(request,'Password does not match')
            return redirect('reset')
    else:
        return render(request,'reset.html')