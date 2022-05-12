from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db.models import Max
from firesale.forms.item_form import CreateItemForm
from firesale.forms.personal_form import PersonalForm, UpdatePersonalForm
from firesale.forms.offer_form import OfferForm
from firesale.forms.contact_form import ContactForm
from firesale.forms.payment_form import PaymenyForm
from firesale.models import Item, ItemImage, Image, Message, Offer, PersonalInformation
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

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
        if request.method == 'GET':
            if 'search' in request.GET:
                search = request.GET['search']
            if 'sortby' in request.GET:
                sortby = request.GET['sortby']
        form = CreateItemForm()
    items = Item.objects.filter(name__icontains=search) if search else Item.objects.all()

    if sortby == 'price':
        items = Item.objects.raw(f'''SELECT fi.id, offer.price FROM firesale_item fi
    JOIN firesale_offer offer ON offer.item_id = fi.id
        WHERE offer.price = (SELECT MAX(o.price)
            FROM firesale_offer o WHERE o.item_id = fi.id)
        {f"AND LOWER(fi.name) LIKE LOWER('%%{search}%%')" if search else ''}
    ORDER BY offer.price DESC;''')
    else:
        items = items.order_by('name')

    __offers = {}
    #print("PersonalInformation:", request.user.PersonalInformation)
    for relate in items:
        offers = Offer.objects.filter(item_id=relate.id)
        __offers[relate] = offers.aggregate(Max('price'))['price__max'] or 'No offers yet.'



    personal_info = PersonalInformation.objects.filter(auth_user_id=request.user.id).first()
    user_image = Image.objects.filter(id=personal_info.user_image_id).first()


    return render(request, 'firesale/dashboard.html', {
        'title': title,
        'search': search or '',
        'form': form,
        'items': items,
        'offers': __offers,
        'personal_info': personal_info,
        'user_image': user_image
    })

@login_required
def inbox(request):
    messages = Message.objects.filter(to=request.user.id)
    personal_info = PersonalInformation.objects.filter(auth_user_id=request.user.id).first()
    user_image = Image.objects.filter(id=personal_info.user_image_id).first()
    return render(request, 'firesale/inbox.html', {
        'messages': messages,
        'personal_info': personal_info,
        'user_image': user_image
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
    personal_info = PersonalInformation.objects.filter(auth_user_id=request.user.id).first()
    user_image = Image.objects.filter(id=personal_info.user_image_id).first()

    items = Item.objects.filter(seller=request.user.id)
    related = items.select_related()

    __offers = {}

    for relate in items:
        offers = Offer.objects.filter(item_id=relate.id)
        __offers[relate] = offers.aggregate(Max('price'))['price__max'] or 'No offers yet.'



    return render(request, 'firesale/dashboard.html', {
        'personal_info': personal_info,
        'title': 'My Items:',
        'form': form,
        'offers': __offers,
        'items': items,
        'user_image': user_image
    })

@login_required
def edit_profile(request, id):
    instance = get_object_or_404(PersonalInformation, auth_user_id=id)
    if request.method == 'POST':
        form = UpdatePersonalForm(data=request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        print(1)
    else:
        form = UpdatePersonalForm(instance=instance)
    personal_info = PersonalInformation.objects.filter(auth_user_id=request.user.id).first()
    user_image = Image.objects.filter(id=personal_info.user_image_id).first()
    return render(request, 'firesale/edit_profile.html', {
        'personal_info': personal_info,
        'form': form,
        'id': id,
        'user_image':user_image
    })


@login_required
def item(request, item_id):
    images = []
    if request.method == 'POST':
        post = request.POST
        form = OfferForm(data={
            'item': Item.objects.filter(id=item_id).first(),
            'is_accepted': False,
            'user_offering': request.user,
            'price': post['price'],
        })
        if form.is_valid():
            form.save()
            return redirect('/dashboard')

    else:
        item_images = ItemImage.objects.filter(item_id=item_id)

        for item_image in item_images:
            image_filter = Image.objects.filter(id=item_image.image_id)
            for image in image_filter:
                images.append(image.url)

        form = OfferForm(initial={
            'item': Item.objects.filter(id=item_id).first(),
            'is_accepted': 0,
            'user_offering': request.user
        })
    item = Item.objects.filter(id=item_id).first()
    personal_info = PersonalInformation.objects.filter(auth_user_id=request.user.id).first()
    user_image = Image.objects.filter(id=personal_info.user_image_id).first()
    offers = Offer.objects.filter(item_id=item.id)

    return render(request, 'firesale/item.html', {
        'item': item,
        'images': images,
        'max_price': offers.aggregate(Max('price'))['price__max'],
        #'offer_id': offers.aggregate(Max('price'))['id'],
        'offers': offers,
        'personal_info': personal_info,
        'form': form,
        'user_image': user_image
    })

@login_required
@csrf_exempt
def checkout(request, item_id):
    item = Item.objects.filter(id=item_id).first()
    if request.method == 'POST':
        post = request.POST
        print("POST:", str(post))
        #print('POST ACTION:', post.action)
        if 'action' in post and 'offer_id' in post:
            action = post['action']
            offer_id = post['offer_id']
            offer = Offer.objects.filter(id=offer_id).first()
            offerer = User.objects.filter(id=offer.user_offering.id).first()

            if action == 'accept':
                rejected_offers = Offer.objects.filter(item_id=item_id).exclude(id=offer_id)
                accept_msg = Message(to=offerer, message=f'Your offer on {item.name} has been accepted! %{item_id}')
                for rejection in rejected_offers:
                    reject_msg = Message(to=User.objects.filter(id=rejection.user_offering.id).first(), message=f'Your offer on {item.name} has been rejected!')
                    reject_msg.save()
                accept_msg.save()
            elif action == 'reject':
                reject_msg = Message(to=offerer, message=f'Your offer on {item.name} has been rejected!')
                reject_msg.save()
        return redirect('/dashboard')

    else:
        personal_info = PersonalInformation.objects.filter(auth_user_id=request.user.id).first()
        user_image = Image.objects.filter(id=personal_info.user_image_id).first()
        contact_form = ContactForm()
        paymeny_form = PaymenyForm()
        return render(request, 'firesale/checkout.html', {
            'item': item,
            'personal_info': personal_info,
            'user_image': user_image,
            'contact_form': contact_form,
            'payment_form': payment_form,
        })
