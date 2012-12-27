Archiver_crawler
============
A collection of tools to parse Wayback Machine of [Internet Archive] (www.archive.org) to get the historical content of web page.
Only the original content of HTML (or other format) content of the web page is downloaded, without the referred objects.

By xiamingc,SJTU - chenxm35@gmail.com

Requirements
------------

Python 2.6+ (<3)

lxml 2.3+

html5lib 0.95+

Programs
------------

`crawler.py` -- to extract the URLs of websites from Internet Archive for content download later.

`retriever.py` -- to downlad the page content with the URLs output by `crawler.py`

`batch.py` -- to run the `retriever.py` in a batch mode across multiple crawler generated files

`siteInfoCrawler.py` -- unfinished; Originally aimed to fetch the history statistics about one site from Alexa.com.
However, this service (http://www.alexa.com/faqs/?p=41) needs to be paid and I make a break about this program.
Someone who is interested in this can contact me to join the project.


Usage of Crawler
------------

If you have python and required packages installed, you can run with python script:

    python crawler.py urlfile


In windows (win64) environment without python installed, you can run the command below:

    dist/crawler.exe urlfile


To build other windows versions of crawler, you can use setup script:

    python setup_exe.py
    
You may need to put matched version of "gdiplus.dll" and "msgcr90.dll" in the foder dll.

The generated distribution locates in "dist" folder, and the crawled historical urls locates in "results".

Usage of Retriever
------------

The same requirements with crawler, with python installed, you can run `retriever` with:

    python retriever.py inputfile

where the inputfile is an individual file output by crawler.

The download pages will locates in folder `retriever_results` created in the program root folder; 
and a subfolder will be created for each inputfile with the same name.

Usage of Libcrawler
------------

Main interface for `crawler.py` for parsing the historical urls of a site:

    for a url:
        generate a SiteDB object by parse_wayback(url)
        call sitedb_obj.dump(stored folder name) to dump the modified version of web page content by Achieve.org
        call sitedb_obj.dump_live(stored folder name) to dump the original version of web page content by Achieve.org
	
For more information about the difference about the modified and original versions, please refer to:
http://faq.web.archive.org/page-without-wayback-code/


Log Information Above ERROR
------------

Note: the frequencies given by my running over ~180K logging information of my project.

libcrawler.py:

    ERROR: "Invalid timestamp of wayback url: %s" 
    Meaning: which means the regex expression can't match the year number from the historical URLs.
    Solution: check the URL manually and find the error reason.
    Frequency: ~ 0%
    
crawler.py:

    No these logging information
    
retriever.py:

    ERROR: "Failed to extract the time string. The url must in the format like: http://web.archive.org/web/19990117032727/google.com/"
    Meaning: which means the regex expression can't match the year number from the historical URLs.
    Solution: check the URL manually and find the error reason.
    Frequency: ~ 0%
    
    ERROR: "Open page error: %s: %s" 
    Meaning: urllib2 can't open this URL occurs. Multiple reasons may lead to the failure: the swayback server is down; or connection
    is block by third party; or something else;
    Solution: check the URL manually or rerun the program at another time.
    Frequency: ~ 14%
    
    ERROR: "Read content error: %s: %s"
    Meaning: read content error of file object of urllib2.open(). Some reason may be the uncompleted content when reading.
    Solution: check the URL manually
    Frequency: ~ 0%
    
    ERROR: "Save redirected page error: [{0}]{1}: {2}"
    Meaning: fail to save the redirected page indicated by the first dumping.
    Solution: check the URL manually
    Frequency: ~ 0.1%
    
    ERROR: "Fail to extract timestamp: %s"
    Meaning: which means the regex expression can't match the exact numbers of the URL about year, month, day, hour, minute, second.
    This is a strong matching action.
    Solution: check the URL manually
    Frequency: ~ 0%
    
    
    

