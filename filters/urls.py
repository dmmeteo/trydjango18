from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add/$', views.add, name='add'),
    url(r'^conf/$', views.conf, name='conf')
]
