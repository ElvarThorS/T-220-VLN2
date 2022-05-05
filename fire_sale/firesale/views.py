from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from firesale.forms.item_form import CreateItemForm
from . import models


# Create your views here.
def index(request):
    return render(request, 'firesale/index.html')


def login(request):
    return render(request, 'firesale/login.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        print("FORM META:", form.model)
        #user_info = models.User()
        if form.is_valid():
            #user = User(data={})
            form.save()

            print("FORM:", form.data)
            return redirect('/login')
    return render(request, 'firesale/register.html', {
        'form': UserCreationForm(),
    })

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = CreateItemForm(data=request.POST)
        if form.is_valid():
            form.save()
            seller = request.user

    else:
        form = CreateItemForm()
    return render(request, 'firesale/dashboard.html', {
        'form': form
    })
'''
@login_required
def dashboard(request):
    return render(request, 'firesale/dashboard.html')
'''
def inbox(request):
    return render(request, 'firesale/inbox.html')

def my_items(request):
    return render(request, 'firesale/my_items.html')

def edit_profile(request):
    return render(request, 'firesale/edit_profile.html')
