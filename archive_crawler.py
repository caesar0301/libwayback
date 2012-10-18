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

# parser = argparse.ArgumentParser(description="Parse the historical\
# version URLs of a web page in Weyback (http://wayback.archive.org/).\
# ")
# parser.add_argument("pagelist", type=str, help="A plain file containing\
# the addresses of web pages.")
# args = parser.parse_args()

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

def parse_canlendar(wbcal):
	""" Parse teh calendar toolkit
	@wbcal: the calendar division, which identified by id="wbCalendar"
	"""
	if not etree.iselement(wbcal):
		print 'Not Element object.'
		return []
	calOver = wbcal.find("./{*}div[@id='calOver']")
	for child in calOver.getchildren():
		print child.attrib['id']

#html_doc = open_url(wayback_search_prefix + '*/www.sina.com.cn')
wholepage = ''
if wholepage != None:
	parser = html5lib.HTMLParser(tree = treebuilders.getTreeBuilder("lxml"))
	html_doc = parser.parse(open("sinares"))	# offline file for test
	body = html_doc.find("./{*}body")
	position_div = body.find("./{*}div[@id='position']")
	wayback_sketch = position_div.find("./{*}div[@id='wbSearch']/{*}div[@id='form']/{*}div[@id='wbMeta']/{*}p[@class='wbThis']")
	wayback_url = wayback_sketch.getchildren()[-1].attrib['href']
	wayback_cal = position_div.find("./{*}div[@id='wbCalendar']")
	# Parse the calendar
	parse_canlendar(wayback_cal)










