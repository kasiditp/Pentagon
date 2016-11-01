from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
import string
import random
from base.auth import Auth
from models import User
import hashlib


# Create your views here.
def login_view(request):
    return render(request, 'pages/member/login.html')


def register_view(request):
    return render(request, 'pages/member/register.html')


def profile_view(request):
    unique_id = request.session['user_unique_id']
    user = User.objects.get(unique_id=unique_id)
    return render(request, 'pages/member/profile.html',{"user" : user})


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    password_md5 = hashlib.md5(password).hexdigest()
    user = User.objects.filter(username=username, password=password_md5)
    if user is not None:
        Auth.login(request, user[0])
        return HttpResponseRedirect(reverse('home:index'))
    else:
        return render(request, 'pages/member/login.html', {"error": "Please check your information!!"})


def add_new_user(request):
    print "enter add user function"
    if request.method == 'POST':
        unique_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        username = request.POST['username']
        password = request.POST['password']
        re_password = request.POST['re_password']
        sex = 2
        if request.POST['gender'] == 'male':
            sex = 1

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        birthdate = request.POST['birthdate']
        email = request.POST['email']
        address = request.POST['address']
        user = User.objects.filter(username=username)
        if user is not None:
            return render(request, 'pages/member/register.html', {"error": "This username is already exist!"})
        if  username == '' or password == '' or re_password == '' or first_name == '' or last_name == '' or birthdate == '' or email == '' or address == '':
            return render(request, 'pages/member/register.html' , {"error":"Please input your information to all fields!"})
        if password != re_password:
            return render(request, 'pages/member/register.html', {"error": "Password and confirm password field must be the same!"})

        new_user = User.objects.create(unique_id = unique_id , username = username ,password = hashlib.md5(password).hexdigest(),email=email,sex=sex,birth_date=birthdate,first_name=first_name,last_name=last_name,address=address)

    return render(request, 'pages/member/register.html')


def change_password(request):
    if request.method == 'POST':
        unique_id = request.session['user_unique_id']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']

        if new_password != confirm_new_password:
            return render(request, 'pages/member/profile.html', {"error": "New password and confirm new password field must be the same!"})
        else:
            user = User.objects.get(unique_id=unique_id)
            user.password = hashlib.md5(new_password).hexdigest()
            user.save()

    return render(request, 'pages/member/profile.html', {"success": "Successfully change password!"})


def change_general(request):
    if request.method == 'POST':
        unique_id = request.session['user_unique_id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        birthdate = request.POST['birthdate']
        email = request.POST['email']
        address = request.POST['address']

        user = User.objects.get(unique_id=unique_id)
        if first_name != '':
            user.first_name = first_name
        if last_name != '':
            user.last_name = last_name
        if birthdate != '':
            user.birth_date = birthdate
        if email != '':
            user.email = email
        if address != '':
            user.address = address
        user.save()

    return render(request, 'pages/member/profile.html', {"success": "Successfully change information!"})


def success(request):
    return render(request, 'pages/member/success.html')
