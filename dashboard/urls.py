from django.conf.urls import url
from views import *


urlpatterns = [
    url(r'^$', DashboardTemplateView.as_view(), name='about2'),
    url(r'^someview/$', SomeView.as_view(), name='someview'),

    url(r'^book/$', BookListView.as_view(), name='book_list'),
    url(r'^book/create/$', BookCreateView.as_view(), name='book_create'),
    url(r'^book/(?P<slug>[-\w]*)/$', BookDetailView.as_view(), name='book_detail'),
    url(r'^book/(?P<slug>[-\w]*)/update$', BookUpdateView.as_view(), name='book_update'),
    url(r'^book/(?P<slug>[-\w]*)/delete$', BookDeleteView.as_view(), name='book_delete'),
]
