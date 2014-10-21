from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'analytics.views.home', name='home'),
)