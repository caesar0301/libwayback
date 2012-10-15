#!/bin/python
import argparse
import urllib2

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

testurl = 'google.com'
print wayback_search_prefix+testurl
fh = urllib2.urlopen(wayback_search_prefix+testurl)
print fh.read()