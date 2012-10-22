Archiver_crawler
============
A collection of tools to parse Wayback Machine of archive.org to get a historical views of web pages

By xiamingc,SJTU - chenxm35@gmail.com

Requirements
------------

Python 2.6+

lxml

html5lib


Simple usage
------------
If you have python and required packages installed, you can run with python script:

    python crawler.py urlfile


In windows (win64) environment without python installed, you can run the command below:

    dist/crawler.exe urlfile


To build other windows versions of crawler, you can use setup script:

    python setup_exe.py

The generated distribution locates in "dist" folder.

The crawled historical urls locates in "results".