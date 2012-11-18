#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xiamingc'
__email__ = 'chenxm35@gmail.com'

from distutils.core import setup  
import py2exe  
import sys
import shutil
import os

# If run without args, build executables, in quiet mode.
if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-q")

SCRIPTS = ['crawler.py', 'retriever.py', 'retrieverBatch.py']
INCLUDES = ['lxml._elementpath', 'gzip']
DATA_FILES_86 = []
DATA_FILES_64 = ["dll/msvcr90_x64.dll", "dll/gdiplus_x64.dll"]

options = {"optimize" : 2,
          "includes" : INCLUDES,
          }

class Target:
  def __init__(self, **kw):
    self.__dict__.update(kw)
    # for the versioninfo resources
    self.version = "0.2.0"
    self.license = "GPLv2 Licence"
    self.author = __author__
    self.author_email = __email__
    self.copyright = "Copyright (C) 2012 xiamingc, SJTU"
    self.name = "ArchiveCrawler for windows"
    self.url = "https://github.com/caesar0301/archive_crawler"

description = "ArchiveCrawler for win64"
data_files = DATA_FILES_64

consoles = []
for script in SCRIPTS:
  consoles.append(Target(
    description=description,
    data_files = data_files,
    script = script,
    dest_base = script.rsplit('.', 1)[0],
    ))

setup(zipfile=None,
    options = {'py2exe': options},
    console = consoles,
    )