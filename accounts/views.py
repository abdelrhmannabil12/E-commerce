from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import RegisterationForm
from .models import *
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
    return render(request,'login.html')
def logout(request):
    return 