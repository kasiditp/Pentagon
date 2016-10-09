from django.shortcuts import render
from models import User
from django.db import connection
# Create your views here.


def register_view(request):
    return render(request, 'pages/member/register.html')
