from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'get_current_site': get_current_site,
    })
    return env
