from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add/$', views.add, name='add'),
    url(r'^conf/$', views.conf, name='conf'),
    url(r'^parsed/(?P<doc_id>\w+)/$', views.filter_parser, name='parsed')
]
