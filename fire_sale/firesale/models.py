from django.db import models
from django.contrib.auth import models as auth_models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Image(models.Model):
    url = models.CharField(max_length=16384)

    def __str__(self):
        return self.url


class Condition(models.Model):
    condition = models.CharField(max_length=255)

    def __str__(self):
        return self.condition

class Payment(models.Model):
    card_holder_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    cvc = models.IntegerField()

class PersonalInformation(models.Model):
    auth_user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=255)
    bio = models.CharField(max_length=8192)
    user_image = models.ForeignKey(Image, on_delete=models.CASCADE, default=None, blank=True)
    street_name = models.CharField(max_length=255, blank=True)
    house_number = models.IntegerField(blank=True, default=None)
    country = models.CharField(max_length=255, blank=True, default='ISL')
    postal_code = models.IntegerField(blank=True, default=None)
    payment_info = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True, default=None)


class Item(models.Model):
    name = models.CharField(max_length=255)
    seller = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    description = models.CharField(max_length=8192)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    is_open = models.BooleanField(default=True)


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)


class Offer(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.IntegerField()
    user_offering = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    is_accepted = models.BooleanField()
    def __str__(self):
        return str(self.price)


class Message(models.Model):
    to = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    message = models.CharField(max_length=8192)



class Order(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    buyer = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    rating = models.FloatField(
        default=None,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    price = models.IntegerField()
