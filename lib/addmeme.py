# -*- coding: utf-8 -*-

import time
import urllib
import urllib2
from django.utils import simplejson
from fdb import *
from lib.expandShortUrl import  *
from lib.filter import  *

from lib import  chardet

import hashlib 
from google.appengine.api import urlfetch
from google.appengine.runtime import apiproxy_errors
import re
import logging
import urlparse
from lib.expandShortUrl import  *
 
def webfetch(link, follow_redirects=True, deadline=30, validate_certificate=False):
    try_times = 2
    for i in xrange(try_times):
        try:
            response = urlfetch.fetch(link, follow_redirects=True, deadline=60, validate_certificate=False)
            break
        except apiproxy_errors.OverQuotaError, e:
            time.sleep(2)
        #except urlfetch.InvalidURLError, e:
        #except urlfetch.ResponseTooLargeError, e:
        except Exception, e:
            return logging.debug('Invalid URL: %s' % link)
            return None
    return response
  
def twittervote(link):
    result = webfetch("https://urls.api.twitter.com/1/urls/count.json?url=%s" % (link), deadline=30, validate_certificate=False)
    if result == None:
        return 0
    if result.status_code != 200 :
        return 0
    urlrt = simplejson.loads(result.content)
    if 'count' in urlrt:
        tvote = int(urlrt['count'])
    return tvote

#todo support multi ulrs query
def facebookvote(link):
    #http://graph.facebook.com/?ids=http://news.ycombinator.com,http://google.com
    fvote = 0
    result = webfetch("https://graph.facebook.com/%s" % (link), deadline=30, validate_certificate=False)
    if result == None:
        return 0
    if result.status_code != 200 :
        return 0
    urlrt = simplejson.loads(result.content)
    if type(urlrt) == bool:
        return 0
    if 'shares' in urlrt:
        fvote = int(urlrt['shares'])
    return fvote

def weibovote(link):
   wvote = 0
   #http://hits.sinajs.cn/A1/weiboshare.html?url=http://news.csdn.net/a/20120123/311050.html?bsh_bid=69989592&count=1&appkey=3434422667
   #http://api.t.sina.com.cn/short_url/shorten.json

   src = '3434422667'
   loc = urlparse.urlparse(link)[1]
   if loc != 't.cn':
       response = webfetch("http://api.t.sina.com.cn/short_url/shorten.json?source=%s&url_long=%s" % (src,link))
       jsondata = response.content
       urldata = simplejson.loads(jsondata)
       link = urldata[0]['url_short']

   result = webfetch("http://api.t.sina.com.cn/short_url/share/counts.json?source=3434422667&url_short=%s" % (link), deadline=30, validate_certificate=False)
   if result.status_code != 200 :
        return 0
   urlrt = simplejson.loads(result.content)
   if 'share_counts' in urlrt:
       fvote = int(urlrt['share_counts'])
   return wvote

def linkedinvote(link):
   lvote=0
#http://www.linkedin.com/cws/share-count?url=http://news.ycombinator.com
#IN.Tags.Share.handleCount({"count":0,"url":"http://news.ycombinator.com"}
   return lvote

def deliciovote(link):
   #http://badges.del.icio.us/feeds/json/url/data?hash=1b9d64f92e36860eced9d68ba7b74708 hashlib.md5(url).hexdigest()
   return 0
 
    
def gplusvote(link):
    gvote = 0
    return gvote
    postdata = '[{"method":"pos.plusones.get","id":"p","params":{"nolog":true,"id":"%s","source":"widget","userId":"@viewer","groupId":"@self"},"jsonrpc":"2.0","key":"p","apiVersion":"v1"}]' % link
    result = urlfetch.fetch("https://clients6.google.com/rpc?key=AIzaSyCGpyCL1wDCRnerJrJZKOv8CHIesJV-6gI", payload=postdata, method=urlfetch.POST, headers={'Content-Type': 'application/json'}, deadline=30, validate_certificate=False)
    urlrt = simplejson.loads(result.content)
    gvote = int(urlrt[0]['result']['metadata']['globalCounts']['count'])
    return gvote

filtersite = ["plus.google.com","www.tumblerandtipsy.com", "www.youtube.com", "instagr.am", "twitpic.com", "www.mobypicture.com", "www.huffingtonpost.com", "vb.net", "www.sourcefabric.org", "twitvid.com", "www.facebook.com", "paste.pocoo.org", "www.elietahari.com"]

def geturls(txt):
   
   reurl = re.compile("((http|https)://[\w+]+[\/\w\/\?\&\%\=\#\$\(\)\@\!\_\-\.\:\;\[\]\{\}\>\|\~\^\+\*]+[^\W\s])")
   group = reurl.findall(txt)
   
   links = []
   for link in group:
       link=link[0]

       """ filter google trace code in url """
       end = link.find("\?utm_source")
       if end > 0 :
           link=link[:end]

       site = urlparse.urlparse(link)[1]
       if site in filtersite :
           continue
       if link not in links:
           links.append(link)
   return links

def getTitleLink(link):
    title = u''
    des = u''
    try:
        response = webfetch(link, follow_redirects=True, deadline=30, validate_certificate=False)
    except:
        return None,None

    if response == None:
        return None,None

    content = response.content
    uri = urlparse.urlparse(link)

    loc = uri[1]
    if short(loc):
       link = response.final_url or link
       if not link.startswith('http') :
           return None,None
       if linkitem.all().filter('url =',link).filter('valid =',0).get() != None :
           return None,None

    # filter url like "aaa.com", no site url, focus article
    uri = urlparse.urlparse(link)

    if uri[1] in filtersite :
       return None,None
    if uri[4]  == '':
       if uri[2]  == '':
          return None,None
       if uri[2]  == '/':
          return None,None
       if uri[2]  == '#':
          return None,None
 
    title = re.search('<title>([\S\s]*?)</title>', content, re.IGNORECASE)
    if title == None:
        return None,None
    title = title.group(1)

    if title=='':
        title=link
    if is_snake(title) :  #or is_snake(content):
        url = linkitem()
        url.valid = 0 
        url.url = link
        url.put()
        return None,None
    else:
        url = linkitem()
        url.valid = 1 
        url.url = link
        url.put()
    
    charset = 'utf-8'
    if 'charset' in response.headers:
       charset1 = response.headers['charset']
    else:
       charset1 = 'utf-8'
    
    if len(content) >= (1 * 1024 * 1024):
        return title, link

    try: 
        content = content.decode(charset1, 'ignore')
        charset = charset1
    except:
        try: 
           m_charset = re.search('<meta\s*http-equiv="?Content-Type"? content="text/html;\s*charset=([\w\d-]+?)"', content, re.IGNORECASE)
           charset2 = m_charset.group(1)
           charset = charset2
        except:
           try:
              charset3 = chardet.detect(content)['encoding']
              content = content.decode(charset3,'ignore')
              charset = charset3
           except:
              try:
                   content = content.decode("utf-8",'ignore')
                   charset = 'utf-8'
              except:
                   return None,None
 
    title = title.decode(charset)

    art = article()
    art.title = title
    art.txt = content
    art.url = link
    art.put()

    return title, link
