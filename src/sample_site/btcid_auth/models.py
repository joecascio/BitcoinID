from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BtcIDUser(models.Model):
    """This is a 1-to-1 extension or 'subclass' of User, which gives us a place
    to store the bitcoin address which is a maddeningly few chars too long for a 
    regular django username"""
    btc_id = models.CharField(max_length=40) 
    user = models.OneToOneField(User)
    
    def __unicode__(self):
        return u'%s (%s)' % (self.btc_id, self.user.username)
        
