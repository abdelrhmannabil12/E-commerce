from django.shortcuts import render,redirect
from django.contrib import messages,auth
from .forms import RegisterationForm
from .models import *
from django.contrib.auth.decorators import login_required
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
            return redirect('home')
        else:
            messages.error(request,"wrong password or username , please try again")
            return redirect('login')
    return render(request,'login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,"You are Logged out")
    return redirect('login')