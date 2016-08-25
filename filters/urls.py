from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('filters:add'))),
    url(r'^add/$', views.add, name='add'),
    url(r'^conf/$', views.conf, name='conf')
]