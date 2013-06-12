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

__author__ = 'chenxm'


import argparse
import httplib
import urllib2
import re
import datetime
import math
import unittest
import logging
import time
import os
import os.path
import random
import sys
import html5lib
from html5lib import treebuilders


logger = logging.getLogger("libwayback.waybackretriever")


def _patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial
    return inner
# Patch HTTPResponse.read to avoid IncompleteRead exception
httplib.HTTPResponse.read = _patch_http_response_read(httplib.HTTPResponse.read)


class WaybackRetriever(object):

	def __init__(self):
		pass


	def extract_time_string(self, url):
		p = re.compile(r"\/([1-2]\d{3}\d*)")
		pm = re.search(p, url)
		if pm != None:
			return pm.group(1)
		else:
			# Explicit Error Report
			logger.error("Failed to extract the time string. URL exmaple: http://web.archive.org/web/19990117032727/google.com/")
			return None


	def extract_timestamp(self, url):
		p = re.compile(r"\/([1-2]\d{3}\d*)")
		pm = re.search(p, url)
		if pm == None: return None

		timestr = pm.group(1)
		members = ["0"]*6 ## [year, month, day, hour, minute, second]
		members_limit = [2999, 12, 31, 23, 59, 59]

		i = 0; j = 0
		leap_year = False
		while 0<= i <= len(timestr)-1:
			if j == 0:
				# year
				members[j] = timestr[:4]
				i += 4; j += 1
				leap_year = (int(members[j])%4 == 0 and True or False)
				continue
			elif j == 2:
				# day
				if int(members[j-1]) in [2]: maxv = leap_year == True and 29 or 28
				elif int(members[j-1]) in [1,3,5,7,8,10,12]: maxv = 31
				else: maxv = 30
			else:
				# month, hour, minute, second
				maxv = members_limit[j]

			if 0<= int(timestr[i:i+2]) <= maxv: offset = 2
			elif int(timestr[i:i+2]) > maxv: offset = 1

			members[j] = timestr[i:i+offset]
			i += offset; j += 1
		return datetime.datetime(year=int(members[0]), month=int(members[1]), \
								day=int(members[2]), hour=int(members[3]), \
								minute=int(members[4]), second=int(members[5]))

	def save_page(self, url, savefile):
		"""
		Return the abstract path of savefile if succeed; 
		Otherwise, return None.
		"""
		url = url.rstrip('\r \n')
		try:
			f = urllib2.urlopen(url)
		except urllib2.URLError, reason:
			## Multiple reasons may lead to the failure:
			## Server is down,
			## The wayback didn't archive this page
			## Connection is block by the third person
			logger.error("Open page error: %s: %s" % (reason, url))
			return None
		except:
			logger.error("Open page error: null: %s" % url)
			return None
			
		try:
			fc = f.read()
		except httplib.IncompleteRead:
			logger.error("Read content error: uncompleted content: %s" % url)
			return None
		except:
			logger.error("Read content error: null: %s" % url)
			return None

		## check content
		RE_WRONG_CONTENT = r'(Got an HTTP \d* response at crawl time)'

		pattern = re.compile(RE_WRONG_CONTENT)
		mp = re.search(pattern, fc)
		if mp != None:
			logger.warning("%s: %s" % (mp.group(1), url))
			parser = html5lib.HTMLParser(tree = treebuilders.getTreeBuilder("lxml"))
			html_doc = parser.parse(fc)
			html_body = html_doc.find("./{*}body")
			div_error = html_body.find(".//{*}div[@id='error']")
			redir_a = div_error.find("./{*}p[@class='impatient']/{*}a")
			redir_url = redir_a.get('href')
			try:
				return self.save_page(redir_url, savefile)
			except RuntimeError, detail:
				logger.error("Save redirected page error: [{0}]{1}: {2}".format(detail.errno, detail.strerror, url))
				return None
			except:
				logger.error("Save redirected page error: null: %s" % url)
				return None
		else:
			open(savefile, 'wb').write(fc)
			return os.path.abspath(savefile)
