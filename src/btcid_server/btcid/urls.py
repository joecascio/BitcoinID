from django.conf.urls import patterns, include, url
import id_mgr

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'ids_at_site/(?P<domain>.*)$', 'id_mgr.views.ids_at_site'),
    url(r'^passphrase/$', 'id_mgr.views.passphrase'), 
    url(r'^set_passphrase/$', 'id_mgr.views.set_passphrase'), 
    url(r'^challenge_response/(?P<identity>.*)$', 'id_mgr.views.challenge_response'),
    url(r'^register_id/$', 'id_mgr.views.register_id'),
    # url(r'^btcid/', include('btcid.foo.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
