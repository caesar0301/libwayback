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
import os
import sys
import datetime
import httplib
from subprocess import *

parser = argparse.ArgumentParser(description='')
parser.add_argument("-log", dest="loglevel", default="DEBUG", type=str, help="Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL")
parser.add_argument('URLFOLDER', type=str, help= '')
args = parser.parse_args()
loglevel = args.loglevel
urlfolder = args.URLFOLDER

argv = sys.argv
(name, suffix) = argv[0].rsplit('.', 1)
if suffix == 'py':
	retriever_exe = "./retriever.py"
	cmdstr = "python %s" % retriever_exe
else:
	# suffix == 'exe'
	if name.rsplit('_', 1)[1] == "":
		retriever_exe = ".\\retriever.exe"
	else:
		retriever_exe = ".\\retriever_%s.exe" % name.rsplit('_', 1)[1]
	cmdstr = "%s" % retriever_exe

assert os.path.exists(retriever_exe),"%s not found" % retriever_exe

all_files = []
for root, dirs, files in os.walk(urlfolder):
	for file in files[:]:
		suffix = file.rsplit('.', 1)[1]
		if suffix != 'txt':
			continue
		all_files.append(os.path.join(root, file))

for urlfile in all_files:
	cmd = cmdstr + " -log %s %s" % (0, loglevel.upper(), urlfile)
	print datetime.datetime.now(), ":", cmd
	Popen(cmd, shell = True, stdout = PIPE).communicate()