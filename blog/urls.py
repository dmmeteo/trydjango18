from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', home, name='home_blog'),
    url(r'^add/$', add_post, name='add_post_blog'),
    url(r'^details/(?P<id>\d+)/$', details, name='details_blog'),
]
