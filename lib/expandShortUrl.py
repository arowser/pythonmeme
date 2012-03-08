# -*- coding: utf-8 -*-

from google.appengine.api import urlfetch
from django.utils import simplejson

#get it from http://api.longurl.org/v2/services?format=json
sites = ['y.ahoo.it', 'doiop.com', 'rickroll.it', 'gizmo.do', 'shrten.com', 'pp.gg', 'hmm.ph', 'redirects.ca', 'ub0.cc', 'urlshorteningservicefortwitter.com', 'gl.am', 'totc.us', 'snipr.com', 'href.in', 'ctvr.us', 'lurl.no', 'tinylink.in', 'sp2.ro', 'fire.to', 'moby.to', 'wapo.st', 'zipmyurl.com', 'omf.gd', 'read.bi', 'surl.hu', 'go.9nl.com', 'nsfw.in', 'hurl.ws', 'clck.ru', 'nutshellurl.com', 'conta.cc', 'urls.im', 'srnk.net', 'short.to', 'its.my', 'tcrn.ch', 'liurl.cn', 'onforb.es', 'shorl.com', 'nbc.co', 't.co', 't.cn', 'show.my', 'abcurl.net', 'firsturl.de', 'twurl.nl', 'linkbee.com', 'binged.it', 'pnt.me', 'yhoo.it', u'\u27bd.ws', 'adjix.com', 'bit.ly', 'ping.fm', 'krunchd.com', 'liltext.com', 'huff.to', 'zzang.kr', 'wapurl.co.uk', 'omoikane.net', 'shink.de', 'qlnk.net', 'twiturl.de', '2.gp', '7.ly', 'not.my', u'\u279e.ws', 'bcool.bz', 'urlenco.de', 'url4.eu', 'ta.gd', 'kl.am', 'smsh.me', 'migre.me', 'macte.ch', 'aa.cx', 'hiderefer.com', 'eepurl.com', 'lnk.ms', 'cort.as', 'ur1.ca', 'shortlinks.co.uk', '6url.com', '4ms.me', u'\u2765.ws', 'ow.ly', 'bacn.me', 'cutt.us', 'freak.to', 'updating.me', 'readthis.ca', 'zi.mu', 'cl.lk', 'ulu.lu', 'fa.by', 'yatuc.com', u'\u273f.ws', u'\u2794.ws', 'youtu.be', 'dld.bz', 'cl.ly', 'yuarel.com', 'go.usa.gov', '307.to', 'urlbrief.com', 'tiniuri.com', 'nn.nf', 'dai.ly', u'\u27a8.ws', 'sn.im', 'j.mp', 'surl.co.uk', 'hsblinks.com', 'zurl.ws', 'smallr.com', 'tnij.org', 'qy.fi', 'bsa.ly', 'arst.ch', 'twitterurl.org', 'tl.gd', 'wipi.es', 'liip.to', 'g.ro.lt', 'cot.ag', 'zi.ma', 'lnkurl.com', 'xurl.es', 'moourl.com', 'b2l.me', 'tgr.ph', 'u.mavrev.com', 's7y.us', 'rww.tw', 'twurl.cc', 'politi.co', 'url.az', 'easyuri.com', 'a.gg', 'goshrink.com', 'shrinkify.com', 'shout.to', 'xr.com', 'starturl.com', 'shrunkin.com', 'l9k.net', 'ix.lt', 's4c.in', '1link.in', 'tinyurl.com', 'ad.vu', '3.ly', 'icanhaz.com', 'yep.it', 'dlvr.it', 'chilp.it', 'atu.ca', 'digbig.com', 'is.gd', 'urli.nl', 'retwt.me', 'urlcut.com', 'do.my', 'minurl.fr', 'alturl.com', 'a.nf', 'sameurl.com', 'profile.to', 'mrte.ch', 'rubyurl.com', 'dopen.us', 'mash.to', 'yiyd.com', 'safe.mn', 'jijr.com', 'twitterurl.net', 'tmi.me', 'korta.nu', 'simurl.com', 'slate.me', 'fav.me', 'amzn.to', 'afx.cc', 'lt.tl', 'fff.to', 'fwd4.me', 'su.pr', 'qte.me', 'tbd.ly', 'chzb.gr', 'lnk.gd', 'z0p.de', 'bizj.us', 'dfl8.me', '4url.cc', 'redirx.com', '2tu.us', 'digg.com', 'togoto.us', 'nxy.in', 'fly2.ws', 'tgr.me', 'xrl.us', 'om.ly', 'shar.es', 'ye.pe', 'u76.org', 'flic.kr', 'rurl.org', 'canurl.com', 'nyti.ms', 'reallytinyurl.com', 'wp.me', 'w55.de', 'ri.ms', 'yfrog.com', 'riz.gd', 'fuseurl.com', 'on.cnn.com', 'azc.cc', 'tr.im', 'xurl.jp', 'fon.gs', 'vb.ly', 'rt.nu', 'zz.gd', 'merky.de', 'go.ign.com', 'xrl.in', 't.lh.com', 'htxt.it', 'u.nu', 'tny.com', 'easyurl.net', 'srs.li', 'adf.ly', 'shrt.st', 'snurl.com', 'to.ly', 'miniurl.com', u'\u27a1.ws', 'goo.gl', 'tiny.pl', 'ar.gy', 'shorturl.com', u'\u2729.ws', 'crks.me', 'ptiturl.com', 'bloat.me', 'smurl.name', 'ff.im', 'to.', 'hex.io', 'trunc.it', 'pub.vitrue.com', 'decenturl.com', 'notlong.com', u'\u27af.ws', 'mke.me', 'firsturl.net', 'hulu.com', 'tinyuri.ca', 'shrt.fr', 'lat.ms', 'qu.tc', 'o-x.fr', 'fbshare.me', 'eweri.com', 'fwib.net', 'tra.kz', 'url.ie', 'urlx.ie', 'pli.gs', 'ln-s.ru', 'ru.ly', 'short.ie', 'gurl.es', 'tiny.cc', 'redir.ec', u'\u27b9.ws', 'idek.net', 'ln-s.net', 'tiny.ly', 'tpm.ly', 'bravo.ly', 'r.im', 'budurl.com', 'myloc.me', 'urlborg.com', 'post.ly', 'clop.in', 'tk.', 'toysr.us', 'disq.us', 'vm.lc', 'rb6.me', 'myurl.in', 'snipurl.com', 'twhub.com', 'b23.ru', 'urlzen.com', 'fb.me', 'shrinkr.com', 'twitclicks.com', 'url360.me', 'cliccami.info', 'lru.jp', '1url.com', 'oc1.us', 'tnw.to', 'urlcover.com', '4sq.com', 'sdut.us', 'lnkd.in', 'x.vu', 'zud.me', 'hurl.me', 'clickthru.ca', 'ilix.in', 'flq.us', 'use.my', 'spedr.com', 'usat.ly', 'n.pr', 'on.mktw.net', 'orz.se', 'nblo.gs', 'fuzzy.to', '2big.at', 'cli.gs', u'\u203a.ws', 'klck.me', 'vl.am', 'twirl.at', 'all.fuseurl.com', 'linkbun.ch', 'url.co.uk', 'vgn.am', 'tighturl.com', '0rz.tw']

def long_url(url):
    try:
        result = urlfetch.fetch("http://api.longurl.org/v2/expand?url=%s&format=json&title=1" % (url))
        jsondata = result.content
        return simplejson.loads(jsondata)
    except:
        return None

def expandShortUrl(url):
    return urlfetch.fetch(url).final_url
 
def short(loc):
    if loc in sites:
        return True
    else:
        return False
 
