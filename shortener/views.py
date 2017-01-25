from django.shortcuts import render
from .forms import UrlForm
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import Url
from django.contrib import auth
from django.db.models import F
from django.core.validators import urlsplit, urlunsplit
from django.urls import reverse
from django.db import IntegrityError


def index(request):
    """Main page with form. Take url from form, normalize, add to db and handle all errors."""
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            url_from_form = form.cleaned_data['url']
            # take domain part, lower it and then merge it back, functions from django, so should be safe.
            scheme, netloc, path, query, fragment = urlsplit(url_from_form)
            standardized_url = urlunsplit((scheme, netloc.lower(), path, query, fragment))
            try:
                Url(url=standardized_url,
                    user=auth.get_user_model().objects.order_by('?').first()
                    ).save()
            except IntegrityError as e:
                try:
                    repr(e).index("NOT NULL constraint failed")
                except ValueError:
                    # url already in DB, don't worry.
                    pass
                else:
                    return HttpResponseNotFound('<h1>There are no users.</h1>')
            url = Url.objects.get(url=standardized_url)
            return HttpResponseRedirect(reverse('info_page', args=[url.shortcut]))
        else:
            return render(request, 'shortener/main_form.html', {'form': form})
    else:
        form = UrlForm()
        return render(request, 'shortener/main_form.html', {'form': form})


def redirect_link(request, url_shortcut):
    """Redirect to the correct url."""
    Url.objects.filter(shortcut=url_shortcut).update(counter=F('counter') + 1)
    try:
        url = Url.objects.get(shortcut=url_shortcut)
    except Url.DoesNotExist:
        return HttpResponseNotFound('<h1>Shortcut doesn\'t exist.</h1>')
    return HttpResponseRedirect(url.url)


def info_page(request, url_shortcut):
    """Show info page."""
    try:
        url = Url.objects.get(shortcut=url_shortcut)
    except Url.DoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    return render(request, 'shortener/info.html', {'url': url})
