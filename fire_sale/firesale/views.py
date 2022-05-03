from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'firesale/index.html')


def login(request):
    return render(request, 'firesale/login.html')


def register(request):
    return render(request, 'firesale/register.html')


def dashboard(request):
    return render(request, 'firesale/dashboard.html')

