from django.db import models
from filebrowser.fields import FileBrowseField

class Foobar(models.Model):
    filebrowse = FileBrowseField('file', max_length=255)
    
    def __unicode__(self):
        return u'%s' % self.filebrowse