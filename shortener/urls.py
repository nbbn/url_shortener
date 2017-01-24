from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^!(.*)$', views.info_page, name='info_page'),
    url(r'^(.*)$', views.redirect_link, name='redirect_link'),
]
