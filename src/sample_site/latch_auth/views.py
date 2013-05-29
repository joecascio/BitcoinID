# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.conf import settings
import random

def home(request):
    nonce = str(random.getrandbits(64))
    request.session['latch_nonce'] = nonce
    return render_to_response("home.html", {'nonce': nonce, 'latch_url':settings.LATCH_URL}, 
    context_instance=RequestContext(request))
    
def new_nonce(request):
    nonce = str(random.getrandbits(64))
    request.session['latch_nonce'] = nonce
    return HttpResponse(nonce)
    
def _check_signature(message, public_key, signature):
    return True # for now
    
def login_state(request, pkey):
    """A typical request would look like this
    https://latch_project.org/login_state/1FrTHp5DR3hLAqCVmuzXLmTLkpJFKCAAgP/?sig=D9BC36CC5811053257F53C7261092525
                                          <====== public key ==============>      <===== signature of 'path' ====> 
                             <====================path=====================>
    """
    signature = request.GET['sig']
    print "pkey:", pkey
    print "signature:", signature
    # check the path against the signature to make sure only
    # the owner of the public key can ask for the login state
    if not _check_signature(request.path, pkey, signature):
        return HttpResponseForbidden()
    print "request.user.username:", request.user.username
    if request.user.is_authenticated() and request.user.username == pkey:
        return HttpResponse('true')
    else:
        return HttpResponse('false')

def log_in(request, pkey):
    """The POST body contains a message that includes the session nonce embedded in the page html plus 
    a signature signed with the id holder's private key."""
    return HttpResponse('Not Implemented yet')
        
def register(request, pkey):
    """The POST body contains whatever demographic data the registrant wants to supply, 
    plus the current session nonce and a signature. This example then queries blockexplorer.info
    to determine the addresse's current balance."""
    return HttpResponse('Not Implemented yet')
