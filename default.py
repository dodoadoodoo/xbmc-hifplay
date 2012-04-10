# coding: latin-1                                                                                                      
import urllib2
import urllib

import xbmcgui
import xbmcplugin
import xbmcaddon

import re

from xml.dom.minidom import parse, parseString
from BeautifulSoup import BeautifulSoup, SoupStrainer


ARCHIVE_URL = "http://play.hif.se/embed/"
PLAY_URL = "http://play.hif.se/admin/uploads/films/[id].flv"
THUMB_URL = "http://play.hif.se/admin/uploads/pictures/[id]_small.jpg"

__settings__ = xbmcaddon.Addon(id='plugin.video.hifplay')

def list_programs():
    doc = unicode(urllib2.urlopen(ARCHIVE_URL).read(), encoding="utf-8", errors="ignore")
    strainer = SoupStrainer("div", "thumbnails")
    soup = BeautifulSoup(doc, fromEncoding="utf-8", parseOnlyThese=strainer)
    print "Original encoding: %s " % soup.originalEncoding
    print "doc: %s " % soup.prettify()
    programs = soup.findAll("div", "thumb")
    regexp = re.compile(".*id\=([0-9]+)")    
    for program in programs:
        link = program.a.get("href")
        itemid = regexp.search(link).group(1).encode("utf_8")
        url = PLAY_URL.replace("[id]", itemid)
        thumb = THUMB_URL.replace("[id]", itemid)
        title = program.img.get("alt").encode("utf_8")
        add_posts(title, url, thumb=thumb)
    xbmcplugin.endOfDirectory(HANDLE)


def add_posts(title, url, description='', thumb='', isPlayable='true', isFolder=False):
    if title == None:
        title = ""
    else:
        title = title.replace("\n", " ")
    if thumb == None:
        listitem=xbmcgui.ListItem(title)
    else:
        listitem=xbmcgui.ListItem(title, iconImage=thumb)        
    if  description == None:
        listitem.setInfo(type='video', infoLabels={'title': title})
    else:
        listitem.setInfo(type='video', infoLabels={'title': title, 'plotoutline': description})
    listitem.setProperty('IsPlayable', isPlayable)
    listitem.setPath(url)
    return xbmcplugin.addDirectoryItem(HANDLE, url=url, listitem=listitem, isFolder=isFolder)


if (__name__ == "__main__" ):
    MODE=sys.argv[0]
    HANDLE=int(sys.argv[1])
    modes = MODE.split('/')
    list_programs()
