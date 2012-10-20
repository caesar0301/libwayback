#!/bin/python
"""
Library for program Archive_crawler.
Copyright (C) 2012  xiamingc, SJTU -  chenxm35@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import urllib
import urllib2
import html5lib
import re
import os
import datetime
import logging
import time
import random
from lxml import etree
from html5lib import treebuilders

#***********************************
# Global configurations
WAYBACK_SEARCH_PREFIX = 'http://wayback.archive.org/web/'
RE_TIMESTAMP = r'\/([1-2]\d{3})(0\d|1[0-2]|[1-9])([0-2]\d|3[0,1]|[1-9])([0,1]\d|2[0-3]|[1-9])([0-5]\d)?([0-5]\d)?'
#***********************************

#***********************************
# Private utilities
def _sanitize_name(fname):
	return fname.strip('\r \n').replace(".", "_")

def _open_url(url):
	try:
		fh = urllib2.urlopen(url)
		if fh.geturl() != url:
			logging.info("Redirected to: %s" % fh.geturl())
		res = fh.read()
	except urllib2.URLError, reason:
		logging.error("%s: %s" % (url, reason))
		res = None
	return res

def _convert_live_url(url):
	""" See "How can I view a page without the Wayback code in it?"
	http://faq.web.archive.org/page-without-wayback-code/
	"""
	pattern = re.compile(RE_TIMESTAMP)
	mres = re.search(pattern, url)
	return url[:mres.end()] + 'id_' + url[mres.end():]

def _extract_wayback_time(url):
	pattern = re.compile(RE_TIMESTAMP)
	mres = re.search(pattern, url)
	if mres == None:
		return None
	res = [0]*6
	for i in range(0, 6):
		res[i] = mres.group(i+1) != None and int(mres.group(i+1)) or 0
	return datetime.datetime(res[0], res[1], res[2], res[3], res[4], res[5])

def _parse_wayback_page(url):
	his_urls = []
	wholepage = _open_url(url)
	if wholepage == None:
		return his_urls
	parser = html5lib.HTMLParser(tree = treebuilders.getTreeBuilder("lxml"))
	html_doc = parser.parse(wholepage)
	body = html_doc.find("./{*}body")
	position_div = body.find("./{*}div[@id='position']")
	wayback_cal = position_div.find("./{*}div[@id='wbCalendar']")
	calOver = wayback_cal.find("./{*}div[@id='calOver']")
	for month in calOver.findall("./{*}div[@class='month']"):
		for day in month.findall(".//{*}td"):
			day_div = day.find("./{*}div[@class='date tooltip']")
			if day_div != None:
				for snapshot in day_div.findall("./{*}div[@class='pop']/{*}ul/{*}li"):
					his_urls.append(snapshot[0].get('href'))
	return his_urls

#***********************************

class SiteDB(object):
	def __init__(self, url):
		self.url = url
		self.db = {}

	def add_item(self, year, item):
		self[str(year)].append(item)

	def __abspath(self, where):
		abswhere = os.path.abspath(where)
		if not os.path.exists(abswhere):
			os.makedirs(abswhere)
		return abswhere

	def dump(self, where = '.'):
		fn = os.path.join(self.__abspath(where), _sanitize_name(self.url)+'.txt')
		f = open(fn, 'w')
		for key in self.db:
			for line in self[key]:
				f.write(line+'\n')
		f.close()

	def dump_live(self, where = '.'):
		fn = os.path.join(self.__abspath(where), _sanitize_name(self.url)+'.live.txt')
		f = open(fn, 'w')
		for key in self.db:
			for line in self[key]:
				f.write(_convert_live_url(line)+'\n')
		f.close()

	def __getitem__(self, year):
		try:
			self.db[str(year)]
		except KeyError:
			self.db[str(year)] = []
		return self.db[str(year)]

	def __setitem__(self, year, item):
		self.db[str(year)] = item
		
	def __len__(self):
		cnt = 0
		for key in db.keys():
			cnt += len(db[key])
		return cnt

def parse_wayback(siteurl):
	""" Parse historical urls for a web page over years.
	We first determine the year scale that has valid snapshots.
	@Params: siteurl - URL for a web page
	@Return: list of historical urls or None
	"""
	wayback_url = WAYBACK_SEARCH_PREFIX + '*/' + siteurl
	wholepage = _open_url(wayback_url)
	if wholepage == None:
		return None

	parser = html5lib.HTMLParser(tree = treebuilders.getTreeBuilder("lxml"))
	html_doc = parser.parse(wholepage)
	position_div = html_doc.find("./{*}body/{*}div[@id='position']")
	# Parse the earliest snapshot timestamp
	sketchinfo = position_div.find("./{*}div[@id='wbSearch']/{*}div[@id='form']/{*}div[@id='wbMeta']/{*}p[@class='wbThis']")
	first_url = sketchinfo.getchildren()[-1].attrib['href']
	first_year = _extract_wayback_time(first_url).year

	sitedb = SiteDB(siteurl)	# new sitedb
	for year in range(first_year, datetime.datetime.now().year+1):
		time.sleep(random.randint(1,3))	# Be polite to the host server
		# Note: the timestamp in search url indicates the time scale of query:
		# E.g., wildcard * matches all of the items in specific year.
		# If only * is supported, the results of latest year are returned.
		# I found that it returned wrong results if the month and day numbers are small like 0101,
		# so a bigger number is used to match wildly.
		wayback_url_year = "%s%d0601000000*/%s" % (WAYBACK_SEARCH_PREFIX, year, siteurl)
		for item in _parse_wayback_page(wayback_url_year):
			try:
				wayback_year =  _extract_wayback_time(item).year
			except AttributeError:
				logging.error("Invalid timestap of wayback url: %s" % item)
				continue
			if year == wayback_year:
				# To exclude duplicated items that don't match the year
				# By default the results of latest year are returned 
				# if some year hasn't been crawled
				sitedb.add_item(year, item)
	return sitedb

if __name__ == '__main__':
	sitedb = SiteDB('sina.com.cn')
	sitedb.dump('results')