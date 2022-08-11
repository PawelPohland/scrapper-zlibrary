from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError

from zlibrary.book import Book
from zlibrary.library import Library


def save_to_file(path, content):
    try:
        with open(path, "w") as file:
            file.write(content)
    except IOError as error:
        print(f"File error: {error}")


def get_source_page(url):
    page_source = ""

    try:
        response = requests.get(url)
        response.raise_for_status()

        page_source = response.text
        response.close()

    except HTTPError as http_err:
        print(f"HTTP error occured: {http_err}")
        print(f"Response status code: {response.status_code}")
    except Exception as err:
        print(f"An error has occured: {err}")
    finally:
        return page_source


def get_books(url):
    source_page = get_source_page(url)

    if source_page:
        parser = BeautifulSoup(source_page, "html.parser")
        items = parser.select("#searchResultBox .bookRow")

        if items:
            library = Library()

            for item in items:
                book = Book(item)
                book.parse()

                library.add_book(book)

            save_to_file("data.json", library.export_json())
        else:
            raise Exception(f"No books available for {url}")
