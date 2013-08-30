# Create your views here.
from id_mgr.models import *

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.conf import settings
import requests
import datetime
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
import traceback

_passphrase = "heplaysagamewithwhichiamnotfamiliar"
_btcrpc = AuthServiceProxy("http://%s:%s@127.0.0.1:8332" % (settings.BTC_RPC_USER, settings.BTC_RPC_PW))

def _passphrase_available():
    global _passphrase
    return len(_passphrase) > 0
    
def _passphrase_valid(pp):
    result = True
    try:
        _btcrpc.walletpassphrase(pp, 0)
    except JSONRPCException:
        result = False
    _btcrpc.walletlock()
    return result
    
def set_passphrase(request):
    """This is the api call"""
    global _passphrase
    pp = json.loads(request.raw_post_data)['passphrase_input']
    if not _passphrase_valid(pp):
        return HttpResponse('Passphrase invalid.')
    _passphrase = pp
    return HttpResponse('True')

def passphrase(request):
    """This is the UI call to set or reset the passphrase memory for the server."""
    global _passphrase
    if request.method == 'GET':
        return render_to_response('passphrase.html', 
        {'passphrase_available': _passphrase_available() }, 
        context_instance=RequestContext(request))
    if request.method == 'POST':
        if 'clear_passphrase' in request.POST:
            _passphrase = ""
        elif 'passphrase_input' in request.POST:
            pp = request.POST['passphrase_input']
            print "valid?", _passphrase_valid(pp)
            if not _passphrase_valid(pp):
                return render_to_response('passphrase.html', 
                {'passphrase_available': _passphrase_available(), 'error_message': "Passphrase invalid!"}, 
                context_instance=RequestContext(request))
            else:
                _passphrase = pp
    return render_to_response('passphrase.html', 
    {'passphrase_available': _passphrase_available() }, 
    context_instance=RequestContext(request))
        

@csrf_exempt
def ids_at_site(request, domain):
    #if (request.method == 'POST'):
    site_url = domain
    request.session['acceptor_domain'] = domain
    ids_at_site = Identity.objects.filter(identityatsite__site__domain=domain)
    ids_not_at_site = Identity.objects.exclude(id__in=ids_at_site)
    return render_to_response('ids_at_site.html', 
        {'passphrase_available': _passphrase_available(), 
        'ids_at_site':ids_at_site, 'ids_not_at_site': ids_not_at_site, 
        'site':domain})#,context_instance=RequestContext(request))

def _make_challenge_response(challenge, identity, passphrase):
    """returns dictionary containing 'challenge', 'addendum', 'message', 'signature'"""
    # already have the passphrase, use it to sign the challenge response
    addendum = str(datetime.datetime.utcnow())
    message = challenge + addendum
    response = {}
    response['challenge'] = challenge
    response['addendum'] = addendum
    response['message'] = message
    _btcrpc.walletpassphrase(passphrase, 1)
    response['signature'] = _btcrpc.signmessage(identity, message)
    _btcrpc.walletlock()
    return response

# @csrf_exempt
# def challenge_response(request, identity):
#     """Returns either the challenge response or a request to prompt the user for passphrase.
#     The challenge text is in the POST data under 'challenge'"""
#     global _passphrase
#     #print 'challenge_response.POST', request.POST
#     #print _passphrase_available()
#     if not _passphrase_available():
#         # return html asking for passphrase
#         return render_to_response('req_passphrase.html')#, context_instance=RequestContext(request))
#     else:
#         post_data = json.loads(request.raw_post_data)
#         #print 'message to sign:' + post_data['message']
#         try:
#             response = _make_challenge_response(post_data['challenge'], identity, _passphrase)
#         except:
#             tb = traceback.format_exc()
#             print tb
#             raise
#         #print "challenge response:", json.dumps(response)
#         return HttpResponse(json.dumps(response))
#         
#         # r_login = requests.post(domain + "/login", data=challenge_response)
#         # # a successful return from the site should contain a URL with an auth token attached
#         # # this will allow the original tab session in the browser to become logged in
#         # # an unsuccessful return will contain an error message, ideally an informative one. :)
#         # return HttpResponse(r_login.text)

#
@csrf_exempt
def challenge_response(request, identity):
    """Returns either the challenge response or a request to prompt the user for passphrase.
    The challenge text is in the POST data under 'challenge'. This also returns the id's demographic
    data like the handle, first, last names, etc."""
    global _passphrase
    if not _passphrase_available():
        # return html asking for passphrase
        return render_to_response('req_passphrase.html')#, context_instance=RequestContext(request))
    else:
        post_data = json.loads(request.raw_post_data)
        #print 'message to sign:' + post_data['message']
        try:
            response = _make_challenge_response(post_data['challenge'], identity, _passphrase)
        except:
            tb = traceback.format_exc()
            print tb
            raise
        
        #look up the identity and add the demographic data
        id_obj = Identity.objects.get(public_key=identity)
        response['handle'] = id_obj.get_handle()
        response['email'] = id_obj.get_email()
        response['first'] = id_obj.entity.first
        response['middle'] = id_obj.entity.middle
        response['last'] = id_obj.entity.last
        response['suffix'] = id_obj.entity.suffix
        
        return HttpResponse(json.dumps(response))        

@csrf_exempt
def login_pp(request, domain, identity):
    """Basically the retry of a login which contains the passphrase as POST data
    that the browser extension prompted the user for."""
    request.session['passphrase'] = request.POST['passphrase']
    return login(request, domain, identity)
    
def register_id(request):
    
    btcid_url = request.GET['btcid_url']
    print "btcid_url", btcid_url
    # the identity already exists, or this function wouldn't be called
    #id_obj = Identity.objects.get(public_key=identity)
    
    # if IdentityAtSite.objects.filter(site__domain=btcid_url, identity__public_key=identity).exists():
    #     return render_to_response('register_id.html', 
    #     {'error_message': 'Id %s already registered at site %s' % (identity, btcid_url)}, 
    #     context_instance=RequestContext(request))        
    
    if request.method == 'POST':
        
        if 'register_button' in request.POST:
            
            pkey = request.POST['register_button']
            id_obj = Identity.objects.get(public_key=pkey)
            
            print "register post data:", request.POST
        
            #if IdentityAtSite.objects.filter(identity=identity).filter(site__domain=btcid_url).exists():
            # create a record for this id and site
            site, created = Site.objects.get_or_create(domain=btcid_url)
    
    
            # # get or create the associative object
            # id_at_site, created = IdentityAtSite.objects.get_or_create(site=site, identity=id_obj)
        
            # do the registration dance
            # get the challenge from the site
            challenge = requests.get(btcid_url + "/btcid_challenge").text
            try:
                reg_data = _make_challenge_response(challenge, pkey, _passphrase)
            except:
                tb = traceback.format_exc()
                print tb
                raise
            reg_data['handle'] = id_obj.get_handle()
            reg_data['email'] = id_obj.get_email()
            reg_data['first'] = id_obj.entity.first
            reg_data['middle'] = id_obj.entity.middle
            reg_data['last'] = id_obj.entity.last
            reg_data['suffix'] = id_obj.entity.suffix
    
            resp = requests.post(btcid_url + '/btcid_register/' + pkey, data=reg_data, headers={'Content-Type': 'application/json;charset=UTF-8'})
            print "register_id, register return data", resp.text
            resp_data = json.loads(resp.text)
            if resp_data['result'] == 'error':
                return render_to_response('register_id.html', {'error_message': resp_data['reason'],
                'passphrase_available': _passphrase_available(), }, 
                context_instance=RequestContext(request))
        
            
            ias = IdentityAtSite()
            ias.site = site
            ias.identity = id_obj
            ias.save()
            
            redirect_url = btcid_url + '/btcid_register_complete'
            print 'redirect_url', redirect_url
            
            return HttpResponseRedirect(redirect_url)

    else: # GET and everything elses comes here
        # request.session['identity'] = identity
        request.session['acceptor_domain'] = btcid_url
        ids_at_site = Identity.objects.filter(identityatsite__site__domain=btcid_url)
        ids_not_at_site = Identity.objects.exclude(id__in=ids_at_site)
        return render_to_response('register_id.html', 
        {'site': btcid_url, 'ids_at_site': ids_at_site, 'ids_not_at_site': ids_not_at_site,
        'passphrase_available': _passphrase_available(), }, 
        context_instance=RequestContext(request))
            