# -*- coding: utf-8 -*-

import time
import urllib
import urllib2
import simplejson
from fdb import *
from lib.expandShortUrl import  *
from lib.filter import  *
from lib.addmeme import  *

from lib import  chardet

import hashlib 
from google.appengine.api import urlfetch
import re
import logging
import urlparse

import HTMLParser

h= HTMLParser.HTMLParser()

   

def rtMeme(keyword):
    links=[]
    result = webfetch("https://search.twitter.com/search.json?lang=en&links&q=RT%%20%s%%20filter:links&rpp=100" % (keyword), deadline=30, validate_certificate=False)
    if result.status_code != 200 :
        return
    jsondata = result.content
    data = simplejson.loads(jsondata)
    data = data["results"]
    for x in data:
        txt = h.unescape(x['text'])

        if is_snake(txt):
            continue

        links = geturls(txt)

        if len(links) == 0:
            continue

        for link in links:
            title, link = getTitleLink(link)
            if title == None:
                continue

            loc = urlparse.urlparse(link)[1]
            #tvote = 0
            #fvote = 0
            #gvote = 0
            tvote = twittervote(link)
            fvote = facebookvote(link)
            gvote = gplusvote(link)
            
            vote = tvote + fvote + gvote
            if vote < 3:
                continue
            if loc == 'pypi.python.org' and vote < 5:
                continue

            c = item() 
            c.tag = keyword
            c.tvote = tvote
            c.gvote = gvote
            c.fvote = fvote
            c.vote = vote
            c.src = 'twitter'
            c.srcsite = loc
            c.url = link
            c.usr = x['from_user']
            c.title = title
            c.txt = txt
            c.time = int(time.time())
            c.put() 

if __name__=='__main__' :
    rtMeme("#python")
