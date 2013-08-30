# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import random
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from btcid_auth.models import *
import uuid
import traceback
import json
from btcid_auth.backend import check_signature

def home(request):
    return render_to_response("home.html", {'btcid_url':settings.BTCID_URL}, context_instance=RequestContext(request))
    
def btcid_challenge(request):
    try:
        nonce = str(random.getrandbits(64))
        request.session['challenge'] = nonce
        return HttpResponse(nonce)
    except:
        tb = traceback.format_exc()
        print tb
        raise
    
@csrf_exempt
def btcid_login(request, pkey):
    """The POST body contains a message that includes the most recent challenge text
    signed with the id holder's private key. If the signature is valid, this session
    is logged in. If already logged in, it has no effect, if another user is logged in
    on this session, that user will be logged out first, then this user logged in."""
    try:
        try:
            luser = BtcIDUser.objects.get(btc_id=pkey)
            user_w_key = luser.user
        except BtcIDUser.DoesNotExist:
            reason = 'BitcoinIdentity User %s not found.' % (pkey)
            return HttpResponse(json.dumps({'result': 'error', 'reason': reason }))
        curr_user = request.user
    
        # if this is the user already logged in, you're done
        if curr_user.is_authenticated():
            if curr_user.id == user_w_key.id:
                return HttpResponse(json.dumps({'result': 'success'}))
            else:
                # logout current user
                logout(request)

        # user is in the database, check to make sure the challenge returned
        # is the same one we sent to this session
        print 'raw_post_data', request.raw_post_data
        auth_data = json.loads(request.raw_post_data)
        if not auth_data['challenge'] == request.session['challenge']:
            return HttpResponse(json.dumps({'result': 'error', 'reason': 'Challenge Mismatch'}))

        # if the current user is authenticated, it isn't the one we want
        # Since we know there is a user with the offered pkey, after we authenticate,
        # we can log out the current user
        if luser.user.is_active:
            authd_user = authenticate(btcid_id=pkey, message=auth_data['message'], signature=auth_data['signature'])
            assert authd_user.id == luser.user.id
            login(request, authd_user)            

            # # flush any previous auth tokens for this session
            # tokens = BtcIDUserAuthToken.objects.filter(session_key=request.COOKIES['sessionid'])
            # for t in tokens:
            #     t.delete()
            # # and generate a new one
            # auth_token = uuid.uuid4().hex.upper()
            # request.session['auth_token'] = auth_token
            # # attach the auth token to the ID
            # luser_token = BtcIDUserAuthToken()
            # luser_token.luser = luser
            # luser_token.token = auth_token
            # luser_token.session_key = request.COOKIES['sessionid']
            # luser_token.save()

            return HttpResponse(json.dumps({'result': 'success'}))
        else:
            return HttpResponseNotFound(json.dumps({'result': 'error', 'reason': 'User inactive'}))
    except:
         tb = traceback.format_exc()
         print tb
         raise
         
def btcid_state(request, pkey):
    """Returns true if the current session has the user with the pkey id logged in. """
    try:
        luser = BtcIDUser.objects.get(btc_id=pkey)
    except BtcIDUser.DoesNotExist:
        return HttpResponse('False')
    if request.user.is_authenticated() and request.user.id == luser.user.id:
        return HttpResponse('True')
    else:
        return HttpResponse('False')

def logout_user(request):
    """This is used by HTML on the site's pages, not by the BitcoinIdentity extension."""
    logout(request)
    return HttpResponseRedirect("/home")
    
def btcid_logout(request, pkey):
    """Post data contains signed message authenticating this request."""
    try:
        luser = BtcIDUser.objects.get(btc_id=pkey)
    except BtcIDUser.DoesNotExist:
        return HttpResponse('True')
    curr_user = request.user
    if curr_user.is_authenticated():
        if curr_user.id == luser.user.id:
            if _auth_data_valid(request, pkey):
                logout(request)
            else: 
                return HttpResponse('False')
    return HttpResponse('True')

@csrf_exempt
def btcid_register(request, pkey):
    """The POST body contains whatever demographic data the registrant wants to supply, 
    plus the current session nonce and a signature. This example then queries blockexplorer.info
    to determine the address's current balance."""
    try:
        if BtcIDUser.objects.filter(btc_id=pkey).exists():
            return HttpResponse(json.dumps({'result': 'error', 'reason': ("Error: BitcoinIdentity Id %s is already registered." % (pkey))}))
        auth_data = request.POST #json.loads(request.raw_post_data)
        print "btcid_register, auth_data", auth_data
        
        if not 'handle' in auth_data:
            auth_data['handle'] = ('lusr_' + pkey)[0:30]
        else:
            # if the given handle is already used, kick it back to the user
            # Note: this rule is determined by the acceptor site. Some sites may allow duplicate handles
            # because the "real" handle is the bitcoin id, which should never be duplicated
            if User.objects.filter(username=auth_data['handle']).exists():
                return HttpResponse(json.dumps({'result': 'error', 'reason': ("Error: Handle %s is already registered." % (auth_data['handle']))}))
    
        # first check the signature so we don't create a bogus user
        if not check_signature(auth_data['message'], pkey, auth_data['signature']): # or auth_data['challenge'] != request.session['challenge']:
            return HttpResponse({'result': 'error', 'reason': "Error: invalid message signature"} )
        
        # create the user. By not sending a password, the function create_unusable_password is
        # called, which is ok since we won't be using a traditional password
        new_user = User.objects.create_user(auth_data['handle'])
        new_user.first_name = auth_data['first']
        new_user.last_name = auth_data['last']
        new_user.email = auth_data['email']
        new_user.save()
    
        # create the btcid user to go along with it
        btcid_user = BtcIDUser()
        btcid_user.user = new_user
        btcid_user.btc_id = pkey
        btcid_user.save()
    
        # don't login the user just yet, just return success
        # user will use btcid_login to login
        return HttpResponse(json.dumps({'result': 'success'}))
    except:
        tb = traceback.format_exc()
        print tb
    
    return HttpResponse(json.dumps({'result': 'error', 'reason': "Exception"} ))
        