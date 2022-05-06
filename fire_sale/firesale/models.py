from django.db import models
from django.contrib.auth import models as auth_models

# Create your models here.


class Image(models.Model):
    url = models.CharField(max_length=16384)


class Condition(models.Model):
    condition = models.CharField(max_length=255)
    def __str__(self):
        return self.condition


class PersonalInformation(models.Model):
    auth_user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=255)
    bio = models.CharField(max_length=8192)
    user_image = models.ForeignKey(Image, on_delete=models.CASCADE, default=None, blank=True)


class Item(models.Model):
    name = models.CharField(max_length=255)
    seller = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    description = models.CharField(max_length=8192)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)


class Offer(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.IntegerField()
    user_offering = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    is_accepted = models.BooleanField()


class Message(models.Model):
    to = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    message = models.CharField(max_length=8192)
