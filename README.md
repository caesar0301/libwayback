Archiver_crawler
============

![wayback machine](http://archive.org/images/wayback_logo-sm.gif)


A library for parsing Wayback Machine of [Internet Archive] (http://www.archive.org) to get the historical content of web page, for research purpose only.

Only the original content of HTML file of the web page is downloaded, without the embedded web objects.

By xiamingc,SJTU - chenxm35@gmail.com


Requirements
------------

[Python 2.6+ (<3)] (http://www.python.org/)

[lxml 2.3+] (http://lxml.de/)

[html5lib 0.95+] (https://github.com/html5lib)


Programs
------------

`wayback_crawler` -- to extract the URLs of websites from Internet Archive for content download later.

`wayback_retriever` -- to downlad the page content with the URLs output of `wayback_crawler`

`libwayback` -- the underlying library support crawler and retriever programs.



Usage of wayback_crawler
------------

If you have python and required packages installed, you can run as python script:

    python wayback_crawler.py [-l log_level] urlfile



Usage of wayback_retriever
------------

The `wayback_retriever` works on the output of `wayback_crawler`. With a specific file, you can run retriever like:

    python wayback_retriever.py <specific_output_file_of_wayback_crawler>

where the input is an individual file output by crawler.

The download pages will locates in folder `retriever_results` located in current working place; 



Usage of libwayback
------------

This library provides basic functions for crawling Internet Archive. It has the simple structures like:

    libwayback
    |____WaybackCrawler
    |____WaybackRetriever

If you are willing to using libwayback in your project, it's easy to integrate:

    from libwayback import WaybackCrawler, WaybackRetriever

    crawler = WaybackCrawler("www.sjtu.edu.cn")
    crawler.parse(live=False)

    # The `results` of crawler instance contains a dict data structure with 
    # a "year" number being the key and a list of page addresses being the value.

    ret = crawler.results

    # Based on the result of crawler, ie a specific page address, you can use 
    # retriever to download and save it in yor file system:

    retriever = WaybackRetriever()

    for year in ret:
        for url in ret[year]:
            retriever.save_page(url, "saved_file")

NOTE:

* The `live` option of `parse()` is responsible to parsing the live version of a page. 
For more about the difference about the modified and original versions, please refer to:
http://faq.web.archive.org/page-without-wayback-code/ .



About logs
------------

libwayback:

    ERROR: "Invalid timestamp of wayback url: %s" 
    Meaning: which means the regex expression can't match the year number from the historical URLs.
    Solution: check the URL manually and find the error reason.
    Frequency: ~ 0%

    
wayback_retriever:

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
    
    
    

