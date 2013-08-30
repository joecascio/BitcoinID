from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gozer.views.home', name='home'),
    # url(r'^gozer/', include('gozer.foo.urls')),
    url(r'home$', 'btcid_auth.views.home'),
    url(r'btcid_challenge$', 'btcid_auth.views.btcid_challenge'),
    url(r'btcid_login/(?P<pkey>.*)$', 'btcid_auth.views.btcid_login'),
    #url(r'login_reply/(?P<pkey>.*)$', 'btcid_auth.views.login_reply'),
    url(r'btcid_state/(?P<pkey>.*)$', 'btcid_auth.views.btcid_state'),
    url(r'btcid_logout/(?P<pkey>.*)$', 'btcid_auth.views.btcid_logout'),
    url(r'logout_user$', 'btcid_auth.views.logout_user'),
    url(r'btcid_register/(?P<pkey>.*)$', 'btcid_auth.views.btcid_register'),
    url(r'btcid_register_complete$', 'btcid_auth.views.home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
