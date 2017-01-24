from django.shortcuts import render
from .forms import UrlForm
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import Url
from django.contrib import auth


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


def handler(request):
    """Handle requests, try to guess is this just redirect or info page. Check in db and return appropriate result."""
    url = request.path_info[1:]
    if url[0] == '!':
        info_page = True
        url_shortcut = url[1:]
    else:
        info_page = False
        url_shortcut = url

    if Url.objects.filter(shortcut=url_shortcut).exists():
        url = Url.objects.get(shortcut=url_shortcut)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    if info_page is True:
        return render(request, 'shortener/info.html', {'url': url})
    else:
        url.counter += 1
        url.save()
        return HttpResponseRedirect(url.url)
