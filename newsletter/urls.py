urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'newsletter.urls')
]