# -*- coding: utf-8 -*-

import os
import cgi
import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

from lib import html2text

import time
import datetime
import urlparse
import urllib

from django.utils import simplejson
from fdb import *
from lib.addmeme import  *
from datetime import timedelta
 
from django.utils import  feedgenerator

class FeedHandler(webapp.RequestHandler):
    def head(self, *args, **kwargs): 
        self.get(*args, **kwargs) 
        self.response.clear()
    def get(self):
        data = memcache.get("feed")
        if data is not None:
            self.response.out.write(data)
            return
        else:
            entries = item.all().order('-time').fetch(20)
    	self.response.headers['Content-Type'] = 'application/atom+xml'

        title = "pythonmeme.com news"
        link = "/feed/"
        description = "python news feed"

        feed = feedgenerator.Atom1Feed(
               title,
               link,
               description)

        for count, l in enumerate(entries) :
            l.date = datetime.datetime.fromtimestamp(l.time)
            feed.add_item(title =l.title, link=l.url, description = l.txt, pubdate=l.date)
        feedtxt = feed.writeString('utf-8')
    	self.response.out.write(feedtxt)
        memcache.add("feed", data, 3600)

class TopFeedHandle(webapp.RequestHandler):
    def get(self,pageNumber=1):
        pageNumber = int(pageNumber)
	normallist = items.all().order('-published').fetch(100)
        newlist = items.all().order('-published').fetch(10)
        hotlist = items.all().order('-hot').fetch(10)

        its = {}
        its['list'] = normallist
        its['newlist'] = newlist
        its['hotlist'] = hotlist
        its['curpage'] = pageNumber
        its['nextpage']=  pageNumber + 1
        its['rang'] = range(11)[1:]
        path = os.path.join(os.path.dirname(__file__), 'topfeed.html')
        self.response.out.write(template.render(path, its))


class AuthorHandle(webapp.RequestHandler):
    def get(self,Author=None, pageNumber=1):
        pageNumber = int(pageNumber)
        if Author != None:
            Author = urllib.unquote(Author)
            Author = unicode(Author,'utf-8')
        normallist = items.all().filter('author = ', Author).fetch(limit=10, offset = (pageNumber -1 ) * 10)

        newlist = items.all().order('-published').fetch(10)
        hotlist = items.all().order('-hot').fetch(10)

        for l in normallist :
            l.date = datetime.datetime.fromtimestamp(l.published)
        its = {}
        its['list'] = normallist
        its['newlist'] = newlist
        its['hotlist'] = hotlist
        its['curpage'] = pageNumber
        its['nextpage']=  pageNumber + 1
        its['rang'] = range(11)[1:]
        path = os.path.join(os.path.dirname(__file__), 'author.html')
        self.response.out.write(template.render(path, its))

class ArticleHandle(webapp.RequestHandler):
    def get(self, id=None):
        normallist = items.all().filter('google_id = ', id)
        newlist = items.all().order('-published').fetch(10)
        hotlist = items.all().order('-hot').fetch(10)

        for l in normallist :
            l.date = datetime.datetime.fromtimestamp(l.published)

        its = {}
        its['list'] = normallist
        its['newlist'] = newlist
        its['hotlist'] = hotlist
        path = os.path.join(os.path.dirname(__file__), 'article.html')
        self.response.out.write(template.render(path, its))

class submitHandle(webapp.RequestHandler):
    def get(self):
        self.response.out.write('get OK')

    def post(self):
        json_entry = self.request.POST
        entry = item()
        link = json_entry['u']
        title = json_entry['t']
        loc = urlparse.urlparse(link)[1]
        tvote = 0
        fvote = 0
        gvote = 0
        tvote = twittervote(link)
        fvote = facebookvote(link)
        gvote = gplusvote(link)
        vote = tvote + fvote + gvote
        if vote < 3:
            self.redirect("/")
            return
        entry.tag = 'python'
        entry.tvote = tvote
        entry.gvote = gvote
        entry.fvote = fvote
        entry.vote = vote
        entry.src = 'submit'
        entry.srcsite = loc
        entry.url = link
        entry.usr = 'submit'
        entry.title = title
        entry.txt = title
        entry.time = int(time.time())
        entry.put()
                 
        self.redirect("/")

class submitlinkHandle(webapp.RequestHandler):
    def get(self):
        entry = item()
        link = self.request.GET['u']
        title = self.request.GET['t']
        loc = urlparse.urlparse(link)[1]
        tvote = twittervote(link)
        fvote = facebookvote(link)
        gvote = gplusvote(link)
        vote = tvote + fvote + gvote
        if vote < 3:
            self.redirect("/")
            return
        entry.tag = 'python'
        entry.tvote = tvote
        entry.gvote = gvote
        entry.fvote = fvote
        entry.vote = vote
        entry.src = 'bookmark'
        entry.srcsite = loc
        entry.url = link
        entry.usr = 'submit'
        entry.title = title
        entry.txt = title
        entry.time = int(time.time())
        entry.put()
 
        self.redirect("/")

    def post(self):
                
        self.redirect("/")

def getdate(itime):
    now = datetime.datetime.now()
    itime = datetime.datetime.fromtimestamp(itime)
    elapsed = (now - itime)
    if elapsed.days > 365:
        return '%d years ago'  % (elapsed.days / 365)
    elif elapsed.days > 1:                
        return '%d days ago'  % (elapsed.days)
    elif elapsed.seconds > 3600:
        return '%d hours ago'  % (elapsed.seconds / 3600)

class memeHandle(webapp.RequestHandler):
    def head(self, *args, **kwargs): 
        self.get(*args, **kwargs) 
        self.response.clear()
    def get(self, pageNumber=1):
        if 'p' in  self.request.GET:
            pageNumber = self.request.GET['p']
        pageNumber = int(pageNumber)
        data = memcache.get("page%d" % pageNumber)
        if data is not None:
            self.response.out.write(data)
            return
        else:
            normallist = item.all().order('-time').fetch(limit=20, offset=(pageNumber-1) * 20)

        for count, l in enumerate(normallist) :
            l.count = (pageNumber - 1) * 20 + count + 1
            l.date = getdate(l.time)
            if l.src == "twitter":
                l.origin = "http://twitter.com/" + l.usr
            elif l.src == "gplus":
                l.origin = "http://plus.google.com/" + l.usr
            elif l.src == "hacknews":
                l.origin = "http://news.ycombinator.com/"
            elif l.src == "feedbundle":
                l.origin = "https://www.google.com/reader/public/javascript/user/18299983671913107256/bundle/python"
            elif l.src == "submit":
                l.origin = "http://www.pythonmeme.com/bookmarklet"
     
        its = {}
        its['page'] = pageNumber + 1
        its['list'] = normallist
        its['suffix'] = ''
        path = os.path.join(os.path.dirname(__file__), 'meme.html')

        data = template.render(path, its)
        memcache.add("page%d" % pageNumber, data, 2400)
        self.response.out.write(data)

class newestHandle(webapp.RequestHandler):
    def head(self, *args, **kwargs): 
        self.get(*args, **kwargs) 
        self.response.clear()
    def get(self, pageNumber=1):
        if 'p' in  self.request.GET:
            pageNumber = self.request.GET['p']
        pageNumber = int(pageNumber)
        data = memcache.get("newest%d" % pageNumber)
        if data is not None:
            self.response.out.write(data)
            return
        else:
            normallist = item.all().order('-time').fetch(limit=20, offset=(pageNumber-1) * 20)
        
        for count, l in enumerate(normallist) :
            l.count = (pageNumber - 1) * 20 + count + 1
            l.date = getdate(l.time)
            if l.src == "twitter":
                l.origin = "http://twitter.com/" + l.usr
            elif l.src == "plus":
                l.origin = "http://plus.google.com/" + l.usr
            elif l.src == "hacknews":
                l.origin = "http://news.ycombinator.com/"
            elif l.src == "feedbundle":
                l.origin = "https://www.google.com/reader/public/javascript/user/18299983671913107256/bundle/python"
            elif l.src == "submit":
                l.origin = "http://www.pythonmeme.com/bookmarklet"
     
        its = {}
        its['page'] = pageNumber + 1
        its['list'] = normallist
        its['suffix'] = 'newest'
        path = os.path.join(os.path.dirname(__file__), 'meme.html')
        data = template.render(path, its)
        memcache.add("newest%d" % pageNumber, data, 2400)
        self.response.out.write(data)
 
class hotHandle(webapp.RequestHandler):
    def head(self, *args, **kwargs): 
        self.get(*args, **kwargs) 
        self.response.clear()
    def get(self, pageNumber=1):
        if 'p' in  self.request.GET:
            pageNumber = self.request.GET['p']
        pageNumber = int(pageNumber)
        data = memcache.get("hot%d" % pageNumber)
        if data is not None:
            self.response.out.write(data)
            return
        else:
            normallist = item.all().order('-vote').fetch(limit=20, offset=(pageNumber-1) * 20)

        for count, l in enumerate(normallist) :
            l.count = (pageNumber - 1) * 20 + count + 1
            l.date = getdate(l.time)
            if l.src == "twitter":
                l.origin = "http://twitter.com/" + l.usr
            elif l.src == "gplus":
                l.origin = "http://plus.google.com/" + l.usr
            elif l.src == "hacknews":
                l.origin = "http://news.ycombinator.com/"
            elif l.src == "feedbundle":
                l.origin = "https://www.google.com/reader/bundle/user/18299983671913107256/bundle/python"
     
        its = {}
        its['page'] = pageNumber + 1
        its['list'] = normallist
        its['suffix'] = 'hot'
        path = os.path.join(os.path.dirname(__file__), 'meme.html')

        data = template.render(path, its)
        memcache.add("hot%d" % pageNumber, data, 9600)
        self.response.out.write(data)

def main():
    application = webapp.WSGIApplication([
      ('/feed', FeedHandler),
      ('/post', submitHandle),
      ('/submitlink', submitlinkHandle),
      ('/hot', hotHandle),
      ('/newest', newestHandle),
      ('/', memeHandle),
    ], debug=False)

    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()


