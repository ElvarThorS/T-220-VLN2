from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from firesale.forms.item_form import ItemForm
from . import models


# Create your views here.
def index(request):
    return render(request, 'firesale/index.html')


def login(request):
    return render(request, 'firesale/login.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    return render(request, 'firesale/register.html', {
        'form': UserCreationForm()
    })

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save()
            seller = request.user

    else:
        form = ItemForm()
    return render(request, 'fire_sale/dashboard.html', {
        'form': form
    })
'''
@login_required
def dashboard(request):
    return render(request, 'firesale/dashboard.html')
'''
