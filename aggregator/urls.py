from django.conf.urls import url
from . import views

# Here we're defining our urlconf for our needs.
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add/$', views.add, name='add'),
    url(r'^edit/$', views.edit, name='edit')
]
