from django.shortcuts import render


# Create your views here.
def login_view(request):
    return render(request, 'pages/member/login.html')


def login(request):
    return None
