from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse('Hello from index view in firesale app')


def login(request):
    return HttpResponse('Here you will login')


def register(request):
    return HttpResponse('Here you will register a new account')


def dashboard(request):
    return HttpResponse('Dashboard will be here')


def edit_profile(request):
    return HttpResponse('Here you will be able to edit your profile')
