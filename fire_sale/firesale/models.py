from django.db import models
from django.contrib.auth import models as auth_models

# Create your models here.
class PersonalInformation(models.Model):
    name = models.CharField(max_length=255)
    bio = models.CharField(max_length=8192)

class Image(models.Model):
    url = models.CharField(max_length=1024)

class User(models.Model):
    auth_user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE, default=None)
    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)
    user_image = models.ForeignKey(Image, on_delete=models.CASCADE)

class Item(models.Model):
    name = models.CharField(max_length=255)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=8192)
    condition = models.CharField(max_length=255)

class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)


class Offer(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.IntegerField()
    user_offering = models.ForeignKey(User, on_delete=models.CASCADE)
    is_accepted = models.BooleanField()

class Message(models.Model):
    to = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=8192)
