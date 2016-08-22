from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add/$', views.add_post, name='add_post'),
    url(r'^details/(?P<id>\d+)/$', views.details, name='details'),
]
