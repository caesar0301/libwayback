#!/bin/python
import argparse
import urllib
import urllib2
import html5lib
from lxml import etree
from html5lib import treebuilders

#***********************************
# Global configurations
wayback_search_prefix = 'http://wayback.archive.org/web/'
#***********************************

parser = argparse.ArgumentParser(description="Parse the historical\
version URLs of a web page in Weyback (http://wayback.archive.org/).\
")
parser.add_argument("pagelist", type=str, help="A plain file containing\
the addresses of web pages.")
args = parser.parse_args()

def open_url(url):
	try:
		fh = urllib2.urlopen(url)
		# check if redirected...
		if fh.geturl() != url:
			print "{0}\nredirected to: {1}".format(url, fh.geturl())
		res = fh.read()
	except urllib2.URLError, reason:
		print "{0}: {1}".format(url, reason)
		res = None
	return res

html_doc = open_url("http://www.baidu.com")
if html_doc != None:
	parser = html5lib.HTMLParser(tree = treebuilders.getTreeBuilder("lxml"))
	etree_doc = parser.parse(html_doc)
	print etree.tostring(etree_doc)