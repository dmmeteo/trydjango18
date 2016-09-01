from django.conf.urls import url
from .views import *

# Here we're defining our urlconf for our needs.
urlpatterns = [
    url(r'^$', home_aggregator, name='home_source'),
    url(r'^add-source/$', add_aggregator, name='add_source'),
    url(r'^edit-source/$', edit_aggregator, name='edit_source'),
    url(r'^update-source/(?P<doc_id>\w+)/$', update_aggregator, name='update_source'),
    url(r'^parse-source/(?P<doc_title>\w+)/$', parse_aggregator, name='parse_source'),
    url(r'^home-filter/$', home_filter, name='home_filter'),
    url(r'^add-filter/$', add_filter, name='add_filter'),
    url(r'^conf-filter/$', conf_filter, name='conf_filter'),
    url(r'^parsed-filter/(?P<doc_id>\w+)/$', parser_filter, name='parsed_filter'),
    url(r'^update-filter/(?P<doc_id>\w+)/$', update_filter, name='update_filter'),
]
