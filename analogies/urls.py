from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('analogies.views',
    url(r'^all/$', 'index', name="analogies.index"),
    #url(r'^search/$', 'search', name="analogies.search"),
    url(r'^(?P<slug>[\w\-]+)/(?P<id>\d+)/$', 'detail', name="analogies.detail"),
    url(r'^(?P<id>\d+)/$', 'short_url', name="analogies.short_url"),
    url(r'^words/(?P<slug>[\w\-]+)/$', 'item', name="analogies.item"),
)