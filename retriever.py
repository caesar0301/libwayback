#!/bin/python
"""
Subtools for Archive_crawler program.
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

RE_TIMESTAMP_SIMPLE = r"\/([1-2]\d{3}\d*)"
THIS_DESCRIPTION = """
Program to retrieve the HTML web pages of the URLs.
Workflow: domains --in--> |crawler| --out--> urllist --in--> |retriever| --out--> webpages.
The input file of retriever should be any individual output file of crawler.
The output file of retriever will be named like '[inputfilename]_[urltimestamp]'
"""

def _extimestr(url):
	p = re.compile(RE_TIMESTAMP_SIMPLE)
	pm = re.search(p, url)
	if pm != None:
		return pm.group(1)
	else:
		# Explicit Error Report
		logging.error("Failed to extract the time string. The url must in the format like: \
			http://web.archive.org/web/19990117032727/google.com/")
		exit(-1)

def _extimetime(url):
	p = re.compile(RE_TIMESTAMP_SIMPLE)
	pm = re.search(p, url)
	if pm == None:
		return None
	timestr = pm.group(1)
	members = ["0"]*6 ## [year, month, day, hour, minute, second]
	members_limit = [2999, 12, 31, 23, 59, 59]
	i = 0
	j = 0
	leap_year = False
	while 0<= i <= len(timestr)-1:
		if j == 0:
			# year
			members[j] = timestr[:4]
			i += 4
			j += 1
			leap_year = (int(members[j])%4 == 0 and True or False)
			continue
		elif j == 2:
			# day
			if int(members[j-1]) in [2]:
				maxv = leap_year == True and 29 or 28
			elif int(members[j-1]) in [1,3,5,7,8,10,12]:
				maxv = 31
			else:
				maxv = 30
		else:
			# month, hour, minute, second
			maxv = members_limit[j]
		if 0<= int(timestr[i:i+2]) <= maxv:
			offset = 2
		elif int(timestr[i:i+2]) > maxv:
			offset = 1
		members[j] = timestr[i:i+offset]
		i += offset
		j += 1
	return datetime.datetime(year=int(members[0]), month=int(members[1]), \
							day=int(members[2]), hour=int(members[3]), \
							minute=int(members[4]), second=int(members[5]))

def _genprogdir():
	return os.path.split(sys.argv[0])[0]

def _genoutdir():
	outputdir = os.path.join(_genprogdir(), "retriever_results")
	if not os.path.exists(outputdir):
		os.makedirs(outputdir)
	return outputdir

def _genoutname(outputfolder, inputfilename, timestr):
	""" Generate output file name like "[inputfilename]_[urltimestamp].txt"
	"""
	name = inputfilename.rsplit('.', 1)[0]
	newdir = os.path.join(outputfolder, name)
	if not os.path.exists(newdir):
		os.makedirs(newdir)
	outputfilename = "%s_%s.txt" % (name, timestr)
	return os.path.join(newdir, outputfilename)
	
def _savepage(url, savefile):
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
		logging.error("Open page error: %s: %s" % (reason, url))
		return None
	except:
		logging.error("Open page error: null: %s" % url)
		return None
		
	try:
		fc = f.read()
	except httplib.IncompleteRead:
		logging.error("Read content error: Incompleted content: %s" % url)
		return None
	except:
		logging.error("Read content error: null: %s" % url)
		return None

	## check content
	RE_WRONG_CONTENT = r'(Got an HTTP \d* response at crawl time)'
	pattern = re.compile(RE_WRONG_CONTENT)
	mp = re.search(pattern, fc)
	if mp != None:
		logging.warning("%s: %s" % (mp.group(1), url))
		parser = html5lib.HTMLParser(tree = treebuilders.getTreeBuilder("lxml"))
		html_doc = parser.parse(fc)
		html_body = html_doc.find("./{*}body")
		div_error = html_body.find(".//{*}div[@id='error']")
		redir_a = div_error.find("./{*}p[@class='impatient']/{*}a")
		redir_url = redir_a.get('href')
		try:
			return _savepage(redir_url, savefile)
		except RuntimeError, detail:
			logging.error("Save page error: [{0}]{1}: {2}".format(detail.errno, detail.strerror, url))
			return None
		except:
			logging.error("Save page error: null: %s" % url)
			return None
	else:
		open(savefile, 'wb').write(fc)
		return os.path.abspath(savefile)

def retriever_smart(inputfile, years = None, days = None):
	logging.info("Start downloading URLs of %s" % inputfile)
	all_urls = []
	for line in open(inputfile, 'rb'):
		line = line.rstrip('\n')
		if line =='':
			continue
		timestamp = _extimetime(line)
		if timestamp == None:
			logging.error("Fail to extract timestamp: %s" % line)
			continue
		all_urls.append((timestamp, line))
	all_urls.sort(lambda x,y:cmp(x[0],y[0]), None, False)
	## Process the time-scale limitations
	if years != None:
		left_urls = [url for url in all_urls if url[0].year in years ]
	else:
		left_urls = all_urls

	inputfilename = os.path.split(inputfile)[1]
	resultdir = _genoutdir()	# output lies in the same folder with this program
	aday = []
	k = 1 	## url counter
	j = 0	## day counter
	n = 0	## valid day counter
	while k <= len(left_urls):
		url = left_urls[k-1]
		if len(aday) == 0 or url[0].day == aday[0][0].day:
			aday.append(url)
		if k == len(left_urls) or left_urls[k][0].day != aday[0][0].day:
			## process the day to featch the earlies valid web page
			print("Parsing the day: %s/%s/%s" % (aday[0][0].month, aday[0][0].day, aday[0][0].year))
			j += 1
			dl = len(aday)	## total url counter for a day
			i = 1 	## url counter for a day
			while i <= dl:
				time.sleep(0.5)
				outputfile = _genoutname(resultdir, inputfilename, _extimestr(aday[i-1][1]))
				status = _savepage(aday[i-1][1], outputfile)
				if status == None:
					i += 1
					continue
				else:
					n += 1
					break
			# start next day
			aday = []
		k += 1
	logging.info("Finish downloading.")
	logging.info("File %s: %d/%d valid days processed" % (inputfile, n, j))

def _patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial
    return inner
    
parser = argparse.ArgumentParser(description=THIS_DESCRIPTION)
parser.add_argument("-y", dest='yearscale', type=str, help="Year scale to retrieve, e.g. '1999', '1999-2003' or '1999,2003' (without quotation marks)")
parser.add_argument("-p", dest='patched', default=1, type=int, help="If httplib.HTTPResponse.read is patched (default 1) to avoid IncompleteRead error.")
parser.add_argument("-log", dest="loglevel", default="DEBUG", type=str, help="Log level: DEBUG(default), INFO, WARNING, ERROR, CRITICAL")
parser.add_argument("URLFILE", type=str, help="File containing wayback URLs output by the crawler.")
args = parser.parse_args()
loglevel = args.loglevel
patched = args.patched
inputfile = args.URLFILE
yearstr = args.yearscale

if yearstr != None:
	years = []
	for i in yearstr.split(','):
		points = [int(j) for j in i.split('-')]
		if len(points) == 1:
			years.append(int(i))
		elif len(points) > 2:
			print("Wrong year scale. -h for help")
			exit(-1)
		else:
			if points[0] <= points[1]:
				years += range(points[0], points[1]+1)
			else:
				years += range(points[1], points[0]+1)
else:
	years = None

## logging
numeric_level = getattr(logging, loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s',
	filename=os.path.join(_genprogdir(), 'retriever.log'), filemode='a', level=numeric_level)

if patched == 1:
	logging.debug("httplib.HTTPResponse.read patched.")
	# Patch HTTPResponse.read to avoid IncompleteRead exception
	httplib.HTTPResponse.read = _patch_http_response_read(httplib.HTTPResponse.read)

print("{0}: processing {1}".format(str(datetime.datetime.now()), inputfile))
retriever_smart(inputfile, years)