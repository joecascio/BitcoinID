from btcid_auth.models import BtcIDUser
from django.contrib.auth.models import User
from bitcoinrpc.authproxy import AuthServiceProxy
from django.conf import settings

_btc = AuthServiceProxy("http://%s:%s@127.0.0.1:8332" % (settings.BTC_RPC_USER, settings.BTC_RPC_PW))

def check_signature(message, public_key, signature):
    result = _btc.verifymessage(public_key, signature, message)
    return result


class BtcIDBackend(object):
    def get_user(self, btcid_primary_key):
        """Takes a btcid ID and returns the User object that is connected to the BtcIDUser object
        with this id"""
        try:
            # print 'get_user:', btcid_primary_key
            return User.objects.get(id=btcid_primary_key)
        except User.DoesNotExist:
            return None

    def authenticate(self, btcid_id, message, signature):
        """User the bitcoin rpc api to check the message against the signature"""
        try:
            luser = BtcIDUser.objects.get(btc_id=btcid_id)
            if check_signature(message, btcid_id, signature):
                return luser.user
            return None
        except BtcIDUser.DoesNotExist:
            return None

