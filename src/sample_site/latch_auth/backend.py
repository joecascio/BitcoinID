from latch_auth.models import LatchUser
from django.contrib.auth.models import User
from bitcoinrpc.authproxy import AuthServiceProxy
from django.conf import settings

_btc = AuthServiceProxy("http://%s:%s@127.0.0.1:8332" % (settings.BTC_RPC_USER, settings.BTC_RPC_PW))

def check_signature(message, public_key, signature):
    result = _btc.verifymessage(public_key, signature, message)
    return result


class LatchBackend(object):
    def get_user(self, latch_primary_key):
        """Takes a latch ID and returns the User object that is connected to the LatchUser object
        with this id"""
        try:
            # print 'get_user:', latch_primary_key
            return User.objects.get(id=latch_primary_key)
        except User.DoesNotExist:
            return None

    def authenticate(self, latch_id, message, signature):
        """User the bitcoin rpc api to check the message against the signature"""
        try:
            luser = LatchUser.objects.get(btc_id=latch_id)
            if check_signature(message, latch_id, signature):
                return luser.user
            return None
        except LatchUser.DoesNotExist:
            return None

