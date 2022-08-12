from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError

from zlibrary.book import Book
from zlibrary.library import Library
from zlibrary.books_not_found import BooksNotFound

import json


class ScrapperError(Exception):
    def __init__(self, message, *args):
        super().__init__(args)
        self.message = message

    def __str__(self):
        return f"~ Scrapper Error: {self.message}"


class Scrapper:
    def __init__(self):
        self.session = requests.Session()
        self.books = Library()
        self.last_page = None

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
        # TODO
        ...

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

                # pagination - check what is the last possible page to scrap
                if not self.last_page:
                    links = parser.select('.paginator td[align="center"] a')
                    if links:
                        self.last_page = int(links[-1].string)
                    else:
                        self.last_page = 1
            else:
                raise BooksNotFound(url, url_params)

    # scrapps books from given url
    def get_books(self, url, url_params=None, num_of_pages=1):
        if not url_params:
            url_params = {}

        if not num_of_pages:
            num_of_pages = 1

        # get first page + check pagination
        self.get_page(url, url_params)

        if num_of_pages > 1 and self.last_page > 1:
            for page_num in range(1, num_of_pages):
                if page_num >= self.last_page:
                    break

                url_params.update({"page": page_num + 1})
                self.get_page(url, url_params)

    # saves to external file
    def save_to_file(self, path, content):
        try:
            with open(path, "w") as file:
                file.write(content)
        except IOError as error:
            print(f"File error: {error}")

    # saves scrapped books to JSON file
    def save_books_as_json(self, file_path):
        if self.books and self.books.count():
            content = json.dumps(self.books.serialize(), indent=4)
            self.save_to_file(file_path, content)
        else:
            raise ScrapperError("There are no books to save!")

    # saves scrapped books to HTML file
    def save_books_as_html(self, file_path):
        # TODO
        ...
