from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
import string
import random
from base.auth import Auth
from base.views import get_nav_context
from models import User
import hashlib


# Create your views here.
def login_view(request):
    return render(request, 'pages/member/login.html', get_nav_context(request))


def register_view(request):
    return render(request, 'pages/member/register.html', get_nav_context(request))


def profile_view(request):
    unique_id = request.session['user_unique_id']
    user = User.objects.get(unique_id=unique_id)
    return render(request, 'pages/member/profile.html',{"user" : user})




def login(request):
    username = request.POST['username']
    password = request.POST['password']
    password_md5 = hashlib.md5(password).hexdigest()
    print password_md5
    user = User.objects.filter(username=username, password=password_md5)
    if user is not None:
        Auth.login(request, user[0])
        return HttpResponseRedirect(reverse('home:index'))
    else:
        return render(request, 'pages/member/login.html', {"error": "Please check your information!!"})


def logout(request):
    Auth.logout(request)
    return HttpResponseRedirect(reverse('home:index'))


def add_new_user(request):
    if request.method == 'POST':
        generate_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        unique_id = "PT-" + generate_id
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

        if User.objects.filter(username=request.POST['username']).exists():
            return render(request, 'pages/member/register.html',
                          {"error": "This username is already exist!",
                            "password" : password,
                            "confirm_password" : re_password,
                            "birthdate": birthdate,
                            "first_name" : first_name,
                            "last_name" : last_name,
                            "email" : email,
                            "address" : address
                          })
        if  username == '' or password == '' or re_password == '' or first_name == '' or last_name == '' or birthdate == '' or email == '' or address == '':
            return render(request, 'pages/member/register.html' ,
                          {"error":"Please input your information to all fields!",
                               "username" : username,
                               "password": password,
                               "confirm_password": re_password,
                               "birthdate" : birthdate,
                               "first_name": first_name,
                               "last_name": last_name,
                               "email": email,
                               "address": address
                           })
        if password != re_password:
            return render(request, 'pages/member/register.html',
                          {"error": "Password and confirm password field must be the same!",
                               "username" : username,
                               "first_name": first_name,
                               "birthdate": birthdate,
                               "last_name": last_name,
                               "email": email,
                               "address": address
                           })

        new_user = User.objects.create(unique_id = unique_id , username = username ,password = hashlib.md5(password).hexdigest(),email=email,sex=sex,birth_date=birthdate,first_name=first_name,last_name=last_name,address=address)

    return render(request, 'pages/member/register.html' , {"success" : "Registration successful!"})


def change_password(request):
    if request.method == 'POST':
        unique_id = request.session['user_unique_id']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        user = User.objects.get(unique_id=unique_id)

        if new_password != confirm_new_password:
            return render(request, 'pages/member/profile.html', {"error": "New password and confirm new password field must be the same!" , "user" : user})
        elif new_password != '' and confirm_new_password != '':
            user = User.objects.get(unique_id=unique_id)
            user.password = hashlib.md5(new_password).hexdigest()
            user.save()
            return render(request, 'pages/member/profile.html', {"success": "Successfully change password!" , "user" : user})
    return render(request, 'pages/member/profile.html', {"success": "Password not changed" , "user" : user})


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

    return render(request, 'pages/member/profile.html', {"success": "Successfully change information!" , "user" : user})

def change_profile_image(request):
    unique_id = request.session['user_unique_id']
    user = User.objects.get(unique_id = unique_id)



def success(request):
    return render(request, 'pages/member/success.html')
