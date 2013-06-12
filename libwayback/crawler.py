#!/usr/bin/python
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
import urllib2
import re
import datetime
import logging
import time
import random
import html5lib
from html5lib import treebuilders


module_logger = logging.getLogger("libwayback.libcrawler")


def _valid_XML_char_ordinal(i):
	## As for the XML specification, valid chars must be in the range of
	## Char ::= #x9 | #xA | #xD | [#x20-#xD7FF] | [#xE000-#xFFFD] | [#x10000-#x10FFFF]
	## [Ref] http://stackoverflow.com/questions/8733233/filtering-out-certain-bytes-in-python
    return (# conditions ordered by presumed frequency
		0x20 <= i <= 0xD7FF 
	    or i in (0x9, 0xA, 0xD)
	    or 0xE000 <= i <= 0xFFFD
	    or 0x10000 <= i <= 0x10FFFF
	    )


class WaybackCrawler(object):
	
	def __init__(self, url):
		self.server = 'http://wayback.archive.org'
		self.prefix = 'http://wayback.archive.org/web'
		self.url = url
		self.results = {}	# year: [historical_page_urls]


	def get_wayback_page(self, site_url):
		return self.prefix + '/*/' + site_url


	def convert_live_url(self, url):
		"""
		For more information, please refer to "How can I view a page without the Wayback code in it?" at
		http://faq.web.archive.org/page-without-wayback-code/
		"""
		pattern = re.compile(r"\/([1-2]\d{3})\d*")
		mres = re.search(pattern, url)
		return url[0:mres.end()] + 'id_' + url[mres.end():]


	def extract_year(self, wayback_url ):
		pattern = re.compile(r"\/([1-2]\d{3})\d*")
		mres = re.search(pattern, wayback_url)
		if mres == None:
			return None
		return int(mres.group(1))


	def open_url(self, url):
		ret = None
		try:
			fh = urllib2.urlopen(url)
			if fh.geturl() != url: module_logger.info("Redirected to: %s" % fh.geturl())
			ret = fh.read()
		except urllib2.URLError, reason:
			module_logger.error("%s: %s" % (url, reason))
		return ret


	def _parse_wayback_page(self, page_year):
		"""
		Paser all recored web page URLs in specific year.
		"""
		his_urls = []
		wholepage = self.open_url(page_year)
		if wholepage == None: return his_urls

		parser = html5lib.HTMLParser(tree = treebuilders.getTreeBuilder("lxml"))

		try:
			html_doc = parser.parse(wholepage)
		except ValueError:
			wholepage_clean = ''.join(c for c in wholepage if _valid_XML_char_ordinal(ord(c)))
			html_doc = parser.parse(wholepage_clean)

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

		year =  self.extract_year(his_urls[0]) if len(his_urls) > 0 else None

		return (year, his_urls)


	def parse(self, live = False):
		""" 
		Parse historical urls for a web page over years.
		We first determine the year scale that has valid snapshots.
		@Return: list of historical urls or None
		"""
		self._parse_called = True

		wayback_page_whole = self.open_url( self.get_wayback_page(self.url) )
		if wayback_page_whole == None: return None

		parser = html5lib.HTMLParser(tree = treebuilders.getTreeBuilder("lxml"))
		html_doc = parser.parse(wayback_page_whole)

		position_div = html_doc.find("./{*}body/{*}div[@id='position']")
		sketchinfo = position_div.find("./{*}div[@id='wbSearch']/{*}div[@id='form']/{*}div[@id='wbMeta']/{*}p[@class='wbThis']")
		first_url = sketchinfo.getchildren()[-1].attrib['href']
		first_year = self.extract_year(first_url)

		for year in range(first_year, datetime.datetime.now().year+1):
			# Be polite to the host server
			time.sleep(random.randint(1,3))

			# Note: the timestamp in search url indicates the time scale of query:
			# E.g., wildcard * matches all of the items in specific year.
			# If only * is supported, the results of latest year are returned.
			# I found that it returned wrong results if the month and day numbers are small like 0101,
			# so a bigger number is used to match wildly.
			wayback_page_year = "/%s%d0601000000*/%s" % ( self.prefix, year, self.url )
			page_year, his_urls = self._parse_wayback_page(wayback_page_year)

			# To exclude duplicated items that don't match the year
			# By default the results of latest year are returned 
			# if some year hasn't been crawled
			if page_year == None or page_year != year: continue
			module_logger.debug("%s: %d pages found for year %d" % (self.url, len(his_urls), page_year))

			for url in his_urls:
				try:
					page_year =  self.extract_year(url)
				except:
					module_logger.error("Invalid timestamp of wayback url: %s" % url)
					continue
				if year == page_year:
					if live: self.add_item(year, self.convert_live_url(url))
					else: self.add_item(year, url)

		return self.results


	def add_item(self, year, item):
		if item[:4] != 'http': item = (self.server + item)
		self[str(year)].append(item)


	def __getitem__(self, year):
		try:
			self.results[str(year)]
		except KeyError:
			self.results[str(year)] = []
		return self.results[str(year)]


	def __setitem__(self, year, item):
		self.results[str(year)] = item

		
	def __len__(self):
		cnt = 0
		for key in results:
			cnt += len(results[key])
		return cnt



if __name__ == '__main__':
	crawler = WaybackCrawler("www.sjtu.edu.cn")
	crawler.parse(live=False)


# EOF