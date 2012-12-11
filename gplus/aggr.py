# -*- coding: utf-8 -*-

import time
import urllib
import urllib2
import simplejson
from fdb import *

import hashlib 
from google.appengine.api import urlfetch
import re
import logging
from lib.addmeme import  *

def extra_data(data, keyword):
    links=[]
    data = data["items"]
    for x in data:
        txt = x['object']['content']
        start = txt.find("http")
        if ( start < 0):
            continue

        links = geturls(txt)
        if len(links) == 0:
           continue

        for link in links:
            title, link = getTitleLink(link)
            if title == None:
                continue

            loc = urlparse.urlparse(link)[1]
            tvote = twittervote(link)
            fvote = facebookvote(link)
            gvote = gplusvote(link)
            
            vote = tvote + fvote + gvote
            if vote < 3:
                continue

            c = item() 
            c.tag = keyword
            c.tvote = tvote
            c.gvote = gvote
            c.fvote = fvote
            c.vote = vote
            c.src = 'gplus'
            c.srcsite = loc
            c.url = link
            c.usr = x['actor']['displayName']
            c.title = title
            c.txt = txt
            c.time = int(time.time())
            c.put() 

def gpMeme(keyword):
    
    key = 'AIzaSyAVpSVXcEHflXPw9NZvF0PZ0Sqpr_gkkZw'
    result = webfetch("https://www.googleapis.com/plus/v1/activities?lang=en&maxResults=20&orderBy=recent&query=%s&key=%s" % (keyword, key), deadline=30, validate_certificate=False)
    jsondata = result.content
    data = simplejson.loads(jsondata)
    extra_data(data, keyword)
    if "nextLink" in data:
        nextlink = data["nextLink"] + "&key=%s" % key
    else:
        return
    for i in range(4):
       result = webfetch(nextlink, deadline=30, validate_certificate=False)
       jsondata = result.content
       data = simplejson.loads(jsondata)
       nextlink = data["nextLink"] + "&key=%s" % key
       extra_data(data, keyword)

if __name__=='__main__' :
    gpMeme("python")
