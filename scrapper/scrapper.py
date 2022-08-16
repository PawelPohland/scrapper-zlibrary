from bs4 import BeautifulSoup

import requests
from requests.exceptions import HTTPError

from zlibrary.book import Book
from zlibrary.library import Library
from zlibrary.books_not_found import BooksNotFound

from scrapper.scrapper_error import ScrapperError
from scrapper.scrapper_file_mgr import ScrapperFileManager

import json
import re


class Scrapper:
    def __init__(self):
        self.session = requests.Session()
        self.books = Library()
        self.last_page = None
        self.file_mgr = ScrapperFileManager()

    def __del__(self):
        self.session.close()
        del self.session
        del self.books

    # removes all scrapped books
    def clear_scrapped_books(self):
        if self.books:
            self.books.clear_books()

    # returns html for parsing
    def get_source_page(self, url, url_params):
        page_source = ""

        try:
            response = self.session.get(url, params=url_params)
            response.raise_for_status()

            page_source = response.text
            response.close()

            return page_source

        except HTTPError as http_err:
            print(f"HTTP error occured: {http_err}")
            print(f"Response status code: {response.status_code}")
        except Exception as err:
            print(f"An error has occured: {err}")

    # gets download link from parsed book
    def get_download_link(self, url):
        source_page = self.get_source_page(url, url_params={})
        if source_page:
            print(f"~ Parsing download link for: {url}")

            parser = BeautifulSoup(source_page, "html.parser")
            download_button = parser.select_one(".dlButton")
            if download_button:
                dl_link = download_button.get('href', '#')
                dl_link = f"{Book.base_url}{dl_link}" if dl_link != "#" else ""

                return f"{Book.base_url}{dl_link}"

    def get_books_download_links(self):
        for book in self.books.books:
            for file_type in book.files_types:
                dl_link = self.get_download_link(file_type["url"])
                if dl_link:
                    file_type["dl_link"] = dl_link

    # gets last page from pagination (if it exists); pagination is added
    # via JavaScript, thus need to parse script tag that contains
    # pagination configuration (pagesTotal)
    def get_last_page(self, paginator):
        if paginator:
            script = paginator.find_next_sibling(name="script")
            if script:
                pattern = re.compile(r"pagesTotal:\s*(\d+)")
                match = pattern.search(script.get_text(strip=True))
                if match:
                    return int(match.group(1))

        # not found, assume default value of 1
        return 1

    # returns books from given url (single page)
    def get_page(self, url, url_params):
        source_page = self.get_source_page(url, url_params)

        if source_page:
            parser = BeautifulSoup(source_page, "html.parser")
            items = parser.select("#searchResultBox .bookRow")

            print(
                f"Scrapping url: {url}?{'&'.join([f'{param}={value}' for param, value in url_params.items()])}")

            if items:
                for item in items:
                    book = Book(item)
                    book.parse()

                    self.books.add_book(book)

                # pagination - check last possible page to scrap
                if not self.last_page:
                    self.last_page = self.get_last_page(
                        parser.select_one(".paginator"))
            else:
                raise BooksNotFound(url, url_params)

    # scrapps books from given url
    def get_books(self, url, url_params=None, num_of_pages=1, start_from_page=1):
        if not url_params:
            url_params = {}

        if not num_of_pages:
            num_of_pages = 1

        if not start_from_page:
            start_from_page = 1

        url_params["page"] = start_from_page

        # get first page + check pagination
        self.get_page(url, url_params)

        # asterisk (*) means scrap all available pages
        if num_of_pages == "*":
            num_of_pages = self.last_page

        # get the rest of available pages
        # if num_of_pages > 1 and self.last_page > 1:
        #     for page_num in range(1, num_of_pages):
        #         if page_num >= self.last_page:
        #             break

        #         url_params.update({"page": page_num + 1})
        #         self.get_page(url, url_params)

        # get pages base on num_of_pages and start_from_page
        if num_of_pages > 1 and self.last_page > 1:
            last_page_to_read = start_from_page + num_of_pages - 1
            if last_page_to_read > self.last_page:
                last_page_to_read = self.last_page

            for page_num in range(start_from_page + 1, last_page_to_read + 1, 1):
                url_params.update({"page": page_num})
                self.get_page(url, url_params)

    # saves scrapped books to JSON file
    def save_books_as_json(self, file_path):
        if self.books and self.books.count():
            content = json.dumps(self.books.serialize(), indent=4)
            self.file_mgr.save_to_file(file_path, content)
        else:
            raise ScrapperError("There are no books to save!")

    # saves scrapped books to HTML file
    def save_books_as_html(self, file_path, page_title):
        if self.books and self.books.count():
            self.file_mgr.render_html_template(
                path=file_path, page_title=page_title, books=self.books.books)

    def get_books_from_json(self, path):
        books_list = self.file_mgr.get_books_from_json_file(path)
        if books_list:
            self.clear_scrapped_books()

            for book_dict in books_list:
                book = Book()
                book.deserialize(book_dict)
                self.books.add_book(book)
