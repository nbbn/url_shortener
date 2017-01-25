from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^!([A-Za-z0-9]*)$', views.info_page, name='info_page'),
    url(r'^([A-Za-z0-9]*)$', views.redirect_link, name='redirect_link'),
]
