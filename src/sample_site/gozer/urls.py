from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gozer.views.home', name='home'),
    # url(r'^gozer/', include('gozer.foo.urls')),
    url(r'home$', 'latch_auth.views.home'),
    url(r'latch_challenge$', 'latch_auth.views.latch_challenge'),
    url(r'latch_login/(?P<pkey>.*)$', 'latch_auth.views.latch_login'),
    #url(r'login_reply/(?P<pkey>.*)$', 'latch_auth.views.login_reply'),
    url(r'latch_state/(?P<pkey>.*)$', 'latch_auth.views.latch_state'),
    url(r'latch_logout/(?P<pkey>.*)$', 'latch_auth.views.latch_logout'),
    url(r'logout_user$', 'latch_auth.views.logout_user'),
    url(r'latch_register/(?P<pkey>.*)$', 'latch_auth.views.latch_register'),
    url(r'latch_register_complete$', 'latch_auth.views.home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
