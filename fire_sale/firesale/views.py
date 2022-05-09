from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from firesale.forms.item_form import CreateItemForm
from firesale.forms.personal_form import PersonalForm
from firesale.models import Item, ItemImage, Image, Message, Offer

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
            personal.save()
            return redirect('/login')
    return render(request, 'firesale/register.html', {
        'form': UserCreationForm(),
    })

@login_required
def dashboard(request):
    search = None
    sortby = None
    title = 'Items for sale:'
    if request.method == 'POST':
        post = request.POST
        autouser = User()
        autouser.id = request.user.id
        autouser.username = request.user.username
        autouser.first_name = request.user.first_name
        autouser.last_name = request.user.last_name
        autouser.email = request.user.email
        autouser.is_staff = request.user.is_staff
        autouser.is_active = request.user.is_active
        autouser.date_joined = request.user.date_joined
        form = CreateItemForm(data={
            'name': post['name'],
            'description': post['description'],
            'condition': post['condition'],
            'image': post['image'],
            'seller': autouser,
        })
        if form.is_valid():
            item = form.save()
            image = Image(url=post['image'])
            image.save()
            item_image = ItemImage(image=image, item=item)
            item_image.save()
    else:
        if request.method == 'GET' and 'search' in request.GET:
            search = request.GET['search']
        form = CreateItemForm()
    return render(request, 'firesale/dashboard.html', {
        'title': title,
        'search': search or '',
        'form': form,
        'items': Item.objects.filter(name__icontains=search) if search else Item.objects.all()
    })

@login_required
def inbox(request):
    messages = Message.objects.filter(to=request.user.id)
    return render(request, 'firesale/inbox.html', {
        'messages': messages
    })

@login_required
def my_items(request):
    if request.method == 'POST':
        form = CreateItemForm(data=request.POST)
        if form.is_valid():
            form.save()
            seller = request.user

    else:
        form = CreateItemForm()
    return render(request, 'firesale/dashboard.html', {
        'title': 'My Items:',
        'form': form,
        'items': Item.objects.filter(seller=request.user.id),
    })

@login_required
def edit_profile(request):
    return render(request, 'firesale/edit_profile.html')


@login_required
def item(request, item_id):
    item_images = ItemImage.objects.filter(item_id=item_id)
    images = []
    for item_image in item_images:

        image_filter = Image.objects.filter(id=item_image.image_id)
        for image in image_filter:
            images.append(image.url)
    item = Item.objects.filter(id=item_id).first()
    return render(request, 'firesale/item.html', {
        'item': item,
        'images': images,
        'offer': Offer.objects.filter(item_id=item.id).first()
    })
