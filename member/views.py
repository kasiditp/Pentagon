from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from models import User
import hashlib
from django.db import connection


# Create your views here.
def login_view(request):
    return render(request, 'pages/member/login.html')


def login(request):
    return None

def register_view(request):
    return render(request, 'pages/member/register.html')

def profile_view(request):
    return render(request, 'pages/member/profile.html')

def add_new_user(request):
    print "enter add user function"
    if request.method == 'POST' :
        unique_id = '00001'
        username = request.POST['username']
        password = request.POST['password']
        sex = 2
        if request.POST['gender'] == 'male':
            sex = 1

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        birthdate = request.POST['birthdate']
        email = request.POST['email']
        address = request.POST['address']

        new_user = User.objects.create(unique_id = unique_id , username = username ,password = hashlib.md5(password).hexdigest(),email=email,sex=sex,birth_date=birthdate,first_name=first_name,last_name=last_name,address=address)
        new_user.save()

    return render(request, 'pages/member/register.html')




def success(request):
    return render(request, 'pages/member/success.html')
