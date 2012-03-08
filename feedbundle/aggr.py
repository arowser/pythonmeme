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


def feedbundle():
    links=[]
    result = webfetch("https://www.google.com/reader/public/javascript/user/18299983671913107256/bundle/python?n=50", deadline=30, validate_certificate=False)
    if result.status_code != 200 :
        return
    jsondata = result.content
    data = simplejson.loads(jsondata)
    data = data["items"]
    for x in data:
        title = x['title']
        link = x['alternate']['href']
        loc = urlparse.urlparse(link)[1]
        tvote = twittervote(link)
        fvote = facebookvote(link)
        gvote = gplusvote(link)
        
        vote = tvote + fvote + gvote
        if vote < 3:
            continue
        if loc == 'pypi.python.org' and vote < 5:
            continue
        c = item() 
        c.tag = 'python'
        c.tvote = tvote
        c.gvote = gvote
        c.fvote = fvote
        c.vote = vote
        c.src = 'feedbundle'
        c.srcsite = loc
        c.url = link
        c.usr = 'feedbundle'
        c.title = title
        c.txt = title
        c.time = int(x['published'])
        c.put() 

if __name__=='__main__' :
    feedbundle()
