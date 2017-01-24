from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import string
import random


class User(AbstractUser):
    pass


def gen_shortcut():
    unique = False
    if settings.SHORT_URL_LENGTH_BOUNDS[1] < settings.SHORT_URL_LENGTH_BOUNDS[0]:
        exit('you bastard!')
    while unique is not True:
        length = random.randint(settings.SHORT_URL_LENGTH_BOUNDS[0], settings.SHORT_URL_LENGTH_BOUNDS[1])
        number_of_az = length // 2 + 1
        if number_of_az < settings.SHORT_URL_LENGTH_BOUNDS[0]:
            number_of_az = settings.SHORT_URL_LENGTH_BOUNDS[0]
        number_of_nums = length - number_of_az
        rand = ''.join(random.choice(string.ascii_letters) for _ in range(number_of_az))
        rand += ''.join(random.choice(string.digits) for _ in range(number_of_nums))
        try:
            Url.objects.get(shortcut=rand)
        except:
            unique = True
    return rand


class Url(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    shortcut = models.CharField(max_length=settings.SHORT_URL_LENGTH_BOUNDS[1],
                                unique=True,
                                default=gen_shortcut)
    url = models.URLField(unique=True)
    counter = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
