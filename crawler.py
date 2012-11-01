#!/bin/python
"""
Main crawler for program Archive_crawler.
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
import logging
import libcrawler

LOG_FILE = 'crawler.log'

__version__ = """Archive_crawler - Version 0.1
Program to parse historical urls of web page from archive.org.
Copyright (c) 2012 xiamingc, SJTU - chenxm35@gmail.com
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.
"""
print (__version__)
print ("See %s for running information" % LOG_FILE)

# Input arguments
parser = argparse.ArgumentParser(description="Parse the historical version URLs of a web page in Weyback (http://wayback.archive.org/).")
parser.add_argument("--log", dest="loglevel", default="INFO", type=str, help="Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL")
parser.add_argument("urllist", type=str, help="A plain file containing the addresses of web pages.")
args = parser.parse_args()
urllist = args.urllist
loglevel = args.loglevel

# Logging
numeric_level = getattr(logging, loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(format='%(asctime)s - %(name)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s',
					filename=LOG_FILE, filemode='a', level=numeric_level)

for url in open(urllist):
	url = url.rstrip('\r\n')
	if url == '':
		continue
	print ("Crawling %s" % url)
	logging.info('Start parsing: %s' % url)
	sitedb = libcrawler.parse_wayback(url)
	logging.info('Finish parsing: %s' % url)
	if sitedb != None:
		logging.info('Dump records of %s to file %s' % (url, url+'.txt'))
		sitedb.dump('results')
		sitedb.dump_live('results/live')