from django.conf.urls import url
from views import *


urlpatterns = [
    url(r'^$', DashboardTemplateView.as_view(), name='about2'),
    url(r'^someview/$', SomeView.as_view(), name='someview'),
    url(r'^book/$', BookList.as_view(), name='book_list'),
    url(r'^book/(?P<slug>[-\w]*)$', BookDetail.as_view(), name='book_detail'),
]