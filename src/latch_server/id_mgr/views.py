# Create your views here.
from id_mgr.models import *
#import httpclient
import urlparse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect


def ids_at_site(request, domain):
    #if (request.method == 'POST'):
    site_url = domain
    print domain
    qresult = IdentityAtSite.objects.filter(site__domain=domain)
    ids = []
    for ias in qresult:
        site_identity = { "key": ias.identity.public_key, "handle": ias.identity.handle }
        ids.append(site_identity)
    json = "%s" % (ids)
    print json
    response = HttpResponse(json)
    return response

def login(request, domain, identity):
    pass
        # go to the site and get the nonce
#         method = httpclient.GetMethod(site_url + "/login_nonce")
#         method.execute()
#         response = method.get_response()

        
        