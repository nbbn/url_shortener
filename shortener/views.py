from django.shortcuts import render
from .forms import UrlForm
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import Url
from django.contrib import auth
from django.db.models import F


def index(request):
    """Main page with form. Process data from form, check if in DB and add if not. Simple redirect to info page."""
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            url_from_form = form.cleaned_data['url']
            if Url.objects.filter(url=url_from_form).exists():
                url = Url.objects.get(url=url_from_form)
            else:
                user = auth.get_user_model().objects.order_by('?').first()
                if user is None:
                    return HttpResponseNotFound('<h1>There are no users.</h1>')
                url = Url(url=url_from_form, user=user)
                url.save()
            return HttpResponseRedirect('/!{}'.format(url.shortcut))
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
