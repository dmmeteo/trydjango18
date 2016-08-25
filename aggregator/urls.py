from django.conf.urls import url
from . import views

# Here we're defining our urlconf for our needs.
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add/$', views.add, name='add'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^update/(?P<doc_id>\w+)/$', views.update, name='update'),
    url(r'^parse/(?P<doc_title>\w+)/$', views.parse, name='parse'),
]
