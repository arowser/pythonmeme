# -*- coding: utf-8 -*-
from google.appengine.ext import db

class UniqueConstraintViolation(Exception):
    def __init__(self, scope, value):
        super(UniqueConstraintViolation, self).__init__("Value '%s' is not unique within scope '%s'." % (value, scope, ))

class article(db.Model):
         url = db.StringProperty()
         title = db.TextProperty()
         txt = db.TextProperty()
         pubtime = db.IntegerProperty()
         def put(self):
                 if item.get_by_key_name(self.url):
                     return None
                 self._key_name = self.url
                 return db.Model.put(self)
 
class item(db.Model):
         tag = db.StringProperty()
         src = db.StringProperty()
         srcsite = db.StringProperty()
         usr = db.StringProperty()
         url = db.StringProperty()
         tvote = db.IntegerProperty()
         gvote = db.IntegerProperty()
         fvote = db.IntegerProperty()
         vote = db.IntegerProperty()
         title = db.TextProperty()
         txt = db.TextProperty()
         time = db.IntegerProperty()
         md5 = db.StringProperty()
         def put(self):
                 if item.get_by_key_name(self.url):
                     #import logging
                     #logging.warning('put title %s' % self.title)
                     #raise UniqueConstraintViolation("title", self.title)
                     return None
                 self._key_name = self.url
                 return db.Model.put(self)

class comments(db.Model):
        url = db.StringProperty()
        md5 = db.StringProperty()
        comment = db.TextProperty()
class trends(db.Model):
         keyword = db.StringProperty()
         time = db.StringProperty()

class linkitem(db.Model):
         valid = db.IntegerProperty()
         url = db.StringProperty(multiline=True)
         def put(self):
                 if item.get_by_key_name(self.url):
                     return None
                 self._key_name = self.url
                 return db.Model.put(self)
 

