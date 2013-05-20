from django.conf.urls import patterns, include, url
import id_mgr

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^prove/$', 'latch.views.prove'), # expects a POST of the site's latch URL
    # url(r'^latch/', include('latch.foo.urls')),
    url(r'ids_at_site/(?P<domain>.*)$', 'id_mgr.views.ids_at_site'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
