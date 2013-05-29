# Create your views here.
from id_mgr.models import *
#import httpclient
import urlparse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext


def ids_at_site(request, domain):
    #if (request.method == 'POST'):
    site_url = domain
    print domain
    identities_at_site = IdentityAtSite.objects.filter(site__domain=domain)
    return render_to_response('ids_at_site.html', 
        {'identities_at_site':identities_at_site, 'site':domain}, 
        context_instance=RequestContext(request))

def login(request, domain, identity):
    pass
        # go to the site and get the nonce
#         method = httpclient.GetMethod(site_url + "/login_nonce")
#         method.execute()
#         response = method.get_response()

        
