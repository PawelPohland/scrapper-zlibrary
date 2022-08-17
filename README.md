# Scrapper - Z-library - https://z-lib.org/

https://z-lib.org/
https://1lib.pl
https://pl.b-ok.xyz/

## Features

- gets books info from various https://z-lib.org/ pages (search results pages, category pages)
- pulls out data about books: ISBN, title, authors, publisher, url, year, language, download links (file type, size, url)
- books on z-library are listed per file type basis which means that the same book can be listed multiple times, each time for different file type (PDF, EPUB, MOBI, etc.) - scrapper on the other hand, combines such books into one entry
- saves scrapped data to JSON file
- saves scrapped data to HTML file
- can open listing of scrapped books in a default web browser
- can load scrapped books from JSON file and scrap download links
- can mark keywords in book's titles

## Technologies used

- Python (requests, BeautifulSoup, Jinja)
- JSON
- HTML
- CSS

## Dependencies

- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [Requests](https://pypi.org/project/requests/)
- [Jinja2](https://pypi.org/project/Jinja2/)

## Possible improvements

- scrap related books
- add multithreading to run requests in different threads (for instance obtaining download links can be done in different threads)
- remove books whose download links cannot be obtained
- add function to download books
- add command line interface (argparse)
- add graphical user interface (for instance with PyQt)
- add Cron job to scrap data periodically
- send generated reports (html files) to e-mail address
