Yellow Pages Germany
====================

This is a web-scraping project that tries to get phone numbers from https://telefonbuch-suche.com/ .
This is a just for fun project, to help me get better at web-scraping.

Dependencies
------------
* requests
* bs4 (beautifulsoup4)
* time.time()
* sqlite3
* re

Goal
----
Goal is to scrape all names completely with address and phone number (estimate = 60.000.000 names).

ToDo´s
------
- [X] get basic scraping of names
- [X] create readme.txt
- [ ] Error-handling (raspberry ran into first error after ~60.000 names)
- [ ] improve performance (use multi-threading)
- [X] write result into a db instead "city_name".csv files
- [ ] make code more object-oriented
- [X] implement stop-resume functionality
- [ ] implement export functionality

Change-Log
----------
20.02.19:
    * implemented sqlite db to store data
        * new class to interact with database
    * removed class originally designed to hold data
    * read online about lxml being faster than bs4 ... wasted an afternoon
21.02.19
    * implemented stop-resume logic
        * query all distinct cities from db
        * query all streetnames from db whre townname = last name of city in list
        * in main() skip all elem in queries