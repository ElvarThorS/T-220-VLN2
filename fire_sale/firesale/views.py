from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from firesale.forms.item_form import CreateItemForm
from firesale.forms.personal_form import PersonalForm

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

            saved = form.save()
            personal = models.PersonalInformation(name=saved.username, bio='', auth_user_id=saved.id, user_image_id=0)
            print("Personal save:", personal)
            personal.save()
            print("SAVED:", saved.id)
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

@login_required
def inbox(request):
    return render(request, 'firesale/inbox.html')

@login_required
def my_items(request):
    return render(request, 'firesale/my_items.html')

@login_required
def edit_profile(request):
    return render(request, 'firesale/edit_profile.html')
