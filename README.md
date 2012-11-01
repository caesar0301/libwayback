Archiver_crawler
============
A collection of tools to parse Wayback Machine of [Internet Archive] (www.archive.org) to get the historical content of web page.

By xiamingc,SJTU - chenxm35@gmail.com

Requirements
------------

Python 2.6+ (<3)

lxml 2.3+

html5lib 0.95+

Programs
------------

`crawler` -- to extract the URLs of websites from Internet Archive for content download later.
`retriever` -- to downlad the page content with the URLs output by `crawler`


Usage of Crawler
------------

If you have python and required packages installed, you can run with python script:

    python crawler.py urlfile


In windows (win64) environment without python installed, you can run the command below:

    dist/crawler.exe urlfile


To build other windows versions of crawler, you can use setup script:

    python setup_exe.py

The generated distribution locates in "dist" folder.

The crawled historical urls locates in "results".

Usage of Retriever
------------

The same requirements with crawler, with python installed, you can run `retriever` with:

    python retriever.py inputfile

where the inputfile is an individual file output by crawler.

The download pages will locates in folder `retriever_results` created in the program root folder; 
and a subfolder will be created for each inputfile with the same name.