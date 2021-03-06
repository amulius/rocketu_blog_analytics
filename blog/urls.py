from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^blog/$', 'blog.views.blog', name='blog'),
    url(r'^blog/(\d+)/$', 'blog.views.post', name='post'),
    url(r'^blog/tag/(\d+)/$', 'blog.views.tag', name='tag'),
    url(r'^blog/author/(\d+)/$', 'blog.views.author', name='author'),
    url(r'^error/$', 'blog.views.error', name='error'),
)