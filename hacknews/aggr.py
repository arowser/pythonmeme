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

filter_dic = ['python', 'django', 'flask', 'pypy', 'web.py', 'bottle']

def hacknews():
    links=[]
    result = webfetch("http://www.google.com/reader/public/javascript/feed/http://news.ycombinator.com/rss?n=100", deadline=30, validate_certificate=False)
    if result.status_code != 200 :
        return
    jsondata = result.content
    data = simplejson.loads(jsondata)
    data = data["items"]
    for x in data:
        title = x['title']
        for dic in filter_dic:
            if re.search("\\b" + dic + "\\b", title, re.IGNORECASE) is not None:
 
                link = x['alternate']['href']
                loc = urlparse.urlparse(link)[1]
                tvote = 0
                fvote = 0
                gvote = 0
                tvote = twittervote(link)
                fvote = facebookvote(link)
                gvote = gplusvote(link)
                
                vote = tvote + fvote + gvote
 
                c = item() 
                c.tag = 'python'
                c.tvote = tvote
                c.gvote = gvote
                c.fvote = fvote
                c.vote = vote
                c.src = 'hacknews'
                c.srcsite = loc
                c.url = link
                c.usr = 'hacknews'
                c.title = title
                c.txt = title
                c.time = int(x['published'])
                c.put() 

if __name__=='__main__' :
    hacknews()
