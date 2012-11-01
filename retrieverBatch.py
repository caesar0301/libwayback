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
from subprocess import *

parser = argparse.ArgumentParser(description='')
parser.add_argument('URLFOLDER', type=str, help= '')
args = parser.parse_args()
urlfolder = args.URLFOLDER

argv = sys.argv
if argv[0].rsplit('.', 1)[1] == 'py':
	retriever_exe = "./retriever.py"
	cmdstr = "python {0} {1}"
else:
	retriever_exe = r".\\retriever.exe"
	cmdstr = "{0} {1}"

assert os.path.exists(retriever_exe),"%s not found" % retriever_exe

all_files = []
for root, dirs, files in os.walk(urlfolder):
	for file in files[:]:
		suffix = file.rsplit('.', 1)[1]
		if suffix != 'txt':
			continue
		all_files.append(os.path.join(root, file))

for urlfile in all_files:
	cmd = cmdstr.format(retriever_exe, urlfile)
	print cmd
	for line in Popen(cmd, shell = True, stdout = PIPE).stdout:
		print line.strip('\r \n')