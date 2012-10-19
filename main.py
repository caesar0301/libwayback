#!/bin/python
import argparse
import logging
import libcrawler

LOG_FILE = 'crawler.log'

print("Archive_crawler - program to parse historical urls of web page from archive.org.\n" +
	"Version 0.1 @COPYLEFT(2012)\n" +
	"xiamingc, SJTU - chenxm35@gmail.com\n")
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
					filename=LOG_FILE, filemode='w', level=numeric_level)

for url in open(urllist):
	url = url.rstrip('\r\n')
	if url == '':
		continue
	logging.info('Start parsing: %s' % url)
	sitedb = libcrawler.parse_wayback(url)
	logging.info('Finish parsing: %s' % url)
	if sitedb != None:
		logging.info('Dump records of %s to file %s' % (url, url+'.txt'))
		sitedb.dump('results')
		sitedb.dump_live('results_live')