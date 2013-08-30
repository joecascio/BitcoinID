from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse

def prove(request):
    response = HttpResponse("Are you the Keymaster?")
    response['Access-Control-Allow-Origin'] = '*'
    print 'REMOTE_ADDR: %s' % (request.META['REMOTE_ADDR'])
    return response