#!/usr/bin/env python

#Project: Taeniurus irc bot  https://github.com/s1n4/Taeniurus
#RSS module for the Taeniurus bot for parsing the tumblr blog's rss

from xml.dom import minidom
import urllib

def get_value(dom, tag):
    return dom.getElementsByTagName(tag)[1].childNodes[0].nodeValue

def rss(url=None):
    if not url: url = 'http://s1n4.tumblr.com/rss'
    if type(url) is list: url = str(url[0])
    xmlFile = urllib.urlopen(url).read()
    dom = minidom.parseString(xmlFile)
    return get_value(dom, 'title'), get_value(dom, 'link')
