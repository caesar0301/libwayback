#!/usr/bin/python
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
import argparse, logging, os, re, sys

from libwayback import WaybackCrawler


# global logger settings
root_logger = logging.getLogger("libwayback")	# use default 'libwayback' logger to active logging function of libwayback
root_logger.setLevel(logging.ERROR)
handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), "app_crawler_log.txt"))
console = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)-15s %(module)s/%(lineno)d %(levelname)s: %(message)s"))
root_logger.addHandler(handler)
root_logger.addHandler(console)


def _sanitize_name(fname):
	return re.sub(r'[\.\/\\\?#&]', "_", fname.strip('\r \n'))

def _abspath(where):
	abswhere = os.path.abspath(where)
	if not os.path.exists(abswhere): os.makedirs(abswhere)
	return abswhere

def dump_results(url, results, where = '.'):
	fn = os.path.join(_abspath(where), _sanitize_name(url)+'.txt')
	with open(fn, 'w') as f:
		for key in results:
			for line in results[key]:
				f.write(line+'\n')


__about__ = \
"""
Archive_crawler - Version 0.1
Program to parse historical urls of web page from archive.org.
Copyright (c) 2012 xiamingc, SJTU - chenxm35@gmail.com
"""


def runMain():
	print (__about__)

	# Input arguments
	parser = argparse.ArgumentParser(description="Parse the historical version URLs of a web page in Weyback (http://wayback.archive.org/).")
	parser.add_argument('-l', dest="loglevel", default="INFO", type=str, help="Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL")
	parser.add_argument("urllist", type=str, help="A plain file containing the addresses of web pages.")
	args = parser.parse_args()
	urllist = args.urllist
	loglevel = args.loglevel

	if not urllist: parser.print_help(); sys.exit(-1)

	# Logging
	numeric_level = getattr(logging, loglevel.upper(), None)
	if not isinstance(numeric_level, int):
	    print('Invalid log level: %s' % loglevel)
	    parser.print_help(); sys.exit(-1);

	# set logger level
	root_logger.setLevel(numeric_level)

	logger = logging.getLogger("libwayback.app_crawler")

	for url in open(urllist):
		url = url.rstrip('\r\n')
		if url == '': continue
		try:
			logger.info('Start parsing: %s' % url)
			crawler = WaybackCrawler(url)
			crawler.parse()
			logger.info('Finish parsing: %s' % url)
		finally:
			if crawler.results:
				logger.info('Dump records of %s to file %s' % (url, url+'.txt'))
				dump_results(url, crawler.results)


if __name__ == '__main__':
	runMain()

# EOF