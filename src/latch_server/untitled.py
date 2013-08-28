def get_auth_token(request, pkey):
    """The POST body contains a message that includes the most recent challenge text
    signed with the id holder's private key."""
    # first see if public_key is a valid user id
    lusers = LatchUser.objects.filter(btc_id=pkey) 
    if len(lusers) == 0:
        return HttpResponseNotFound('User %s not found in database', pkey)
    luser = lusers[0]
    # user is in the database, check to make sure the challenge returned
    # is the same one we sent to this session
    returned_challenge = request.POST['challenge']
    if returned_challenge != request.session['challenge']:
        return HttpResponseBadRequest('Challenge error')
    # returned challenge matches, get the addendum string that the user
    # appended that will prevent replay attacks, and concat them to make
    # the message that was signed
    returned_addendum = request.POST['addendum']
    reply_message = returned_challenge + returned_addendum
    signature = request.POST['signature']
    # test the message against the signature using the public key
    if not _check_signature(reply_message, pkey, signature):
        return HttpResponseForbidden('Signature error')
    # signature is correct. 
    # if we got here, there's a user with this id, and they're not
    # logged in already, so we can generate an auth token for a session
    # to use to log in
    auth_token = uuid.uuid4().hex.upper()
    # attach the auth token to the ID
    luser_token = LatchUserAuthToken()
    luser_token.luser = luser
    luser_token.token = auth_token
    luser_token.session_key = 'new_issue'
    luser_token.save()
    return HttpResponse(auth_token)
    
def login_with_token(request, pkey, auth_token):
    """If the auth token exists for the luser and it has not been used
    for another session, this function will log that user in and set the
    luser auth token record with this session id. Thenceforth, that auth
    token will be unusable by any other session."""
    try:
        luser = LatchUser.objects.get(btc_id=pkey)
    except DoesNotExist:
        return HttpResponseNotFound('Latch User %s not found.' %(pkey))
    curr_user = request.user
    if curr_user.is_authenticated:
        if curr_user.id == luser.user.id:
            # if auth token is same, just return
            if 'auth_token' in request.session 
                and auth_token == request.session['auth_token']:
                return HttpResponse('True')
            # new auth token. Destroy old one, 
        else: # current user not the one we're trying to log in
            # log current user out
            curr_user.logout(request)
            
    # no user logged in
    try:
        # see if the token is kosher
        auth_token_obj = LatchUserAuthToken.object.get(token=auth_token)
    except (DoesNotExist, MultipleObjectsReturned):
        return HttpResponseNotFound('Invalid Latch Auth Token: %s' % (auth_token))
