from django.contrib import admin
from shortener.models import Url
from django.contrib import auth

admin.site.register(auth.get_user_model())
admin.site.register(Url)
