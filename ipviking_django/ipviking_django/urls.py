from django.conf.urls import patterns, include, url
from ipviking_django.views import HomeView, NextView, AuthView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^auth/$', AuthView.as_view(), name='auth'),
    url(r'^next/$', NextView.as_view(), name = 'next'),
    # url(r'^DjangoGoesToNorway/', include('DjangoGoesToNorway.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
#     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

#     Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
