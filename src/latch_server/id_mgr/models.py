from django.db import models
# Create your models here.
class Entity(models.Model):
    """Represents a person or business entity"""
    default_handle = models.CharField(max_length=100) # eg: 'joecascio'
    prefix = models.CharField(blank=True, max_length=100) # eg: 'Mr.'
    first = models.CharField(blank=True, max_length=100) # eg: 'Joseph' 
    last = models.CharField(blank=True, max_length=100) # eg: 'Cascio'
    middle = models.CharField(blank=True, max_length=100) # eg: 'C.'
    suffix = models.CharField(blank=True, max_length=100) # eg: 'Jr.'
    default_email = models.EmailField(max_length=254)
    
    def __unicode__(self):
        return u'%s : %s %s %s %s %s : %s' % (self.default_handle, self.prefix, self.first, self.middle, self.last, self.suffix, self.default_email)

class Identity(models.Model):
    """The login information that identifies the Entity to a particular web site"""
    entity = models.ForeignKey(Entity) # demographics to use
    handle = models.CharField(max_length=100, blank=True) # can replace the default handle if desired
    public_key = models.CharField(max_length=100) # private key not held in database, obvs.
    email = models.EmailField(blank=True, max_length=254)
    def __unicode__(self):
        return u'%s : %s (%s %s %s)' % (self.handle, self.public_key, self.entity.first, self.entity.middle, self.entity.last)
    
    def get_handle(self):
        if len(self.handle) > 0:
            return self.handle
        return self.entity.default_handle
    
    def get_email(self):
        if len(self.email) > 0:
            return self.email
        return self.entity.default_email

class Site(models.Model):
    domain = models.CharField(max_length=100) # include sub-domains. eg: blog.onlyzuul.org
    def __unicode__(self):
        return u'%s' % (self.domain)

class IdentityAtSite(models.Model):
    """M-to-N relationship. It's possible to have more than one identity at a site,
    and to use the same identity on different sites"""
    site = models.ForeignKey(Site)
    identity = models.ForeignKey(Identity)    
    site_auth_type = models.TextField(blank=True) # if site issues acct#, api key, password, etc
                                                    # this field says what to look for on keychain
    def __unicode__(self):
        return u'%s (%s) at %s' % (self.identity.handle, self.identity.public_key, self.site)
