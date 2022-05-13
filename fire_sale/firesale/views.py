from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db.models import Max, Model, IntegerField, FloatField
from firesale.forms.item_form import CreateItemForm
from firesale.forms.personal_form import PersonalForm, UpdatePersonalForm
from firesale.forms.offer_form import OfferForm
from firesale.forms.contact_form import ContactForm
from firesale.forms.payment_form import PaymentForm
from firesale.forms.order_form import OrderForm
from firesale.models import Item, ItemImage, Image, Message, Offer, PersonalInformation, Payment, Order
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from . import models

'''
    !!!!!!!!!!!Þetta á EKKI að registera sem view!!!!!!!!!!!
'''
def get_user_average(request):
    class Average(Model):
        id = IntegerField(),
        average = FloatField()

    average_rating = Average.objects.raw(f'''SELECT u.id AS id, AVG(o.rating) AS average FROM firesale_order o
    JOIN firesale_item i ON i.id = o.item_id
    JOIN auth_user u ON u.id = i.seller_id
       WHERE i.seller_id = {request.user.id}
        GROUP BY u.id;''')
    average = 'No reviews done.'
    if len(average_rating) != 0:
        average = average_rating[0].average
    return average

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
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
            'is_open': True,
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
        'user_image': user_image,
        'average': get_user_average(request)
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
        'user_image': user_image,
        'average': get_user_average(request)
    })

@login_required
def edit_profile(request, id):

    if request.method == 'POST':
        instance = get_object_or_404(PersonalInformation, auth_user_id=id)
        new_image = Image(url=request.POST['image'])
        new_image.save()
        print("INSTANCE:", instance)
        instance.user_image = new_image
        instance.user_image_id = new_image.id
        instance.name = request.POST['name']
        instance.bio = request.POST['bio']
        instance.save()

    personal_info = PersonalInformation.objects.filter(auth_user_id=request.user.id).first()
    form = UpdatePersonalForm(data={
        'name': personal_info.name,
        'bio': personal_info.bio,
        'image': personal_info.user_image.url
    })

    user_image = Image.objects.filter(id=personal_info.user_image_id).first()
    return render(request, 'firesale/edit_profile.html', {
        'personal_info': personal_info,
        'form': form,
        'id': id,
        'user_image': user_image,
        'average': get_user_average(request)
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
        'user_image': user_image,
        'average': get_user_average(request)
    })

@login_required
@csrf_exempt
def checkout(request, item_id):
    item = Item.objects.filter(id=item_id).first()
    if request.method == 'POST':
        post = request.POST
        print("POST:", str(post))

        if 'action' in post and 'offer_id' in post:
            action = post['action']
            offer_id = post['offer_id']
            offer = Offer.objects.filter(id=offer_id).first() #the accepted offer if accept was pressed
            offerer = User.objects.filter(id=offer.user_offering.id).first()

            if action == 'accept':
                rejected_offers = Offer.objects.filter(item_id=item_id).exclude(id=offer_id)
                accept_msg = Message(to=offerer, message=f'Your offer on {item.name} has been accepted! %{item_id}')
                for rejection in rejected_offers:
                    reject_msg = Message(to=User.objects.filter(id=rejection.user_offering.id).first(), message=f'Your offer on {item.name} has been rejected!')
                    reject_msg.save()
                accept_msg.save()
                offer.is_accepted = True
                offer.item.is_open = False;
                offer.save()
                offer.item.save()
            elif action == 'reject':
                reject_msg = Message(to=offerer, message=f'Your offer on {item.name} has been rejected!')
                reject_msg.save()

            return redirect('/dashboard')
        elif 'full_name' in post and 'street_name' in post and 'house_number' in post and 'country' in post and 'postal_code' in post and 'city' in post:
            # Hér er allt fyrir contact information POST
            contact = ContactForm(data=post)
            if contact.is_valid():
                data = contact.cleaned_data
                personal_info = PersonalInformation.objects.filter(auth_user_id=request.user.id).first()
                personal_info.name = data['full_name']
                personal_info.street_name = data['street_name']
                personal_info.house_number = data['house_number']
                personal_info.country = data['country']
                personal_info.postal_code = data['postal_code']
                personal_info.city = data['city']
                personal_info.save()
            else:
                print("Invalid data!")


            return redirect('/payment-information/' + item_id + '/')

    else:
        personal_info = PersonalInformation.objects.filter(auth_user_id=request.user.id).first()
        user_image = Image.objects.filter(id=personal_info.user_image_id).first()
        contact_form = ContactForm(data={
            'full_name': personal_info.name,
            'street_name': personal_info.street_name,
            'house_number': personal_info.house_number,
            'country': personal_info.country or 'ISL',
            'postal_code': personal_info.postal_code,
            'city': personal_info.city
        })
        payment_form = PaymentForm()
        return render(request, 'firesale/checkout.html', {
            'item': item,
            'personal_info': personal_info,
            'user_image': user_image,
            'contact_form': contact_form,
            'payment_form': payment_form,
            'average': get_user_average(request),
        })


@login_required
@csrf_exempt
def payment_information(request, item_id):
    if request.method == 'POST':
        post = request.POST
        if 'card_holder_name' in post and 'card_number' in post and 'expiration_date' in post and 'cvc' in post:
            # Hér er allt fyrir payment information POST
            personal = PersonalInformation.objects.filter(auth_user_id=request.user.id).first()
            payment = PaymentForm(data=post, instance=Payment.objects.filter(id=personal.payment_info_id).first())
            print("PAYMENT:", payment)
            if payment.is_valid():
                saved = payment.save()
                print("SAVED:", saved)
                personal_info = PersonalInformation.objects.filter(auth_user_id=request.user.id).first()
                personal_info.payment_info_id = saved.id
                personal_info.save()
                return redirect('/review/' + item_id + '/')
            else:
                print("INVALID")
                return redirect(f'/payment-information/{item_id}/')




    item = Item.objects.filter(id=item_id).first()
    personal_info = PersonalInformation.objects.filter(auth_user_id=request.user.id).first()
    user_image = Image.objects.filter(id=personal_info.user_image_id).first()
    payment_info = Payment.objects.filter(id=personal_info.payment_info_id).first()
    payment_form = PaymentForm(instance=payment_info)
    return render(request, 'firesale/payment_information.html', {
        'item': item,
        'personal_info': personal_info,
        'user_image': user_image,
        'payment_form': payment_form,
        'average': get_user_average(request)
    })

@login_required
def review(request, item_id):
    personal_info = PersonalInformation.objects.filter(auth_user_id=request.user.id).first()
    payment_info = Payment.objects.filter(id=personal_info.payment_info_id).first()
    user_image = Image.objects.filter(id=personal_info.user_image_id).first()
    item = Item.objects.filter(id=item_id).first()
    offers = Offer.objects.filter(item_id=item.id)
    offer = offers.filter(is_accepted=True).first()
    if request.method == 'POST':
        order_form = OrderForm(data={
            'item': item.id,
            'buyer': request.user.id,
            'rating': request.POST['rating'],
            'price': offer.price
        })
        if order_form.is_valid():
            order_form.save()
            return redirect('/dashboard/')
        else:
            return render(request, 'firesale/review.html', {
            'item': item,
            'personal_info': personal_info,
            'payment_info': payment_info,
            'user_image': user_image,
            'form': order_form,
            'average': get_user_average(request)
        })
    else:
        order_form = OrderForm()
        return render(request, 'firesale/review.html', {
            'item': item,
            'personal_info': personal_info,
            'payment_info': payment_info,
            'user_image': user_image,
            'form': order_form,
            'average': get_user_average(request)
        })
