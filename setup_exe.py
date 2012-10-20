#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xiamingc'

from distutils.core import setup  
import py2exe  
import sys

# If run without args, build executables, in quiet mode.
if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-q")

INCLUDES = ['lxml._elementpath', 'gzip']
DATA_FILES = ["dll/MSVCR90.dll", "dll/gdiplus.dll"]

options = {"optimize" : 2,
          "includes" : INCLUDES,
          }

setup(name = "archive crawler",
      version = "0.1",
      description = "Program to parse historical urls of web page from archive.org.",
      author = "xiamingc",
      author_email ="chenxm35@gmail.com",
      maintainer = "xiamingc",
      maintainer_email = "chenxm35@gmail.com",
      license = "GPLv2 Licence",
      url = "https://github.com/caesar0301/archive_crawler",

      data_files = DATA_FILES,
      zipfile=None,
      options = {'py2exe': options},
      console = ['crawler.py']
      )