from xml.dom import minidom
import urllib

def getValue(dom, tag) :
	return dom.getElementsByTagName(tag)[1].childNodes[0].nodeValue

def rss(url=None) :
	if not url: url = 'http://s1n4.tumblr.com/rss'
	xmlFile = urllib.urlopen(url).read()
	dom = minidom.parseString(xmlFile)
	return getValue(dom, 'title'), getValue(dom, 'link')

