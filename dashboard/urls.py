from django.conf.urls import url
from views import *


urlpatterns = [
    url(r'^$', DashboardTemplateView.as_view(), name='about2'),
    url(r'^someview/$', SomeView.as_view(), name='someview'),
]