from bs4 import BeautifulSoup
import requests

from book import Book


def save_to_file(path, content):
    with open(path, "w") as file:
        file.write(content)


def get_source_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Something went wrong {response.status_code}!")
    else:
        return response.text


if __name__ == "__main__":
    # try:
    source_page = get_source_page(
        "https://1lib.pl/s/django?yearFrom=2022&yearTo=2022&languages%5B%5D=english")

    if source_page:
        parser = BeautifulSoup(source_page, "html.parser")
        items = parser.select("#searchResultBox .bookRow")
        for item in items:
            book = Book()
            book.parse(item)
            book.print()

    # except Exception as error:
    # print(error)
