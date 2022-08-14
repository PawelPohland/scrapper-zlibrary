import scrapper.scrapper as scrapper


def load_json_and_get_download_links(path):
    scr = scrapper.Scrapper()

    scr.get_books_from_json(path)
    # scr.books.print_books()

    return scr


def get_download_links(path):
    scr = load_json_and_get_download_links(path)

    print("*** Getting download links ***")

    scr.get_books_download_links()
    # scr.books.print_books()
    scr.save_books_as_json(path)


def get_books(url, url_params=None, num_of_pages=1, save_as_json=None):
    scr = scrapper.Scrapper()
    scr.get_books(url, url_params, num_of_pages)
    if save_as_json:
        scr.save_books_as_json(save_as_json)


if __name__ == "__main__":
    try:
        # get_books(url="https://1lib.pl/s/django?yearFrom=2022&yearTo=2022&languages%5B%5D=english")

        # get_books(url="https://1lib.pl/s/django", url_params={"yearFrom": 2022, "yearTo": 2022, "languages%5B%5D": "english", "page": 1}, save_as_json="scrapped_pages/django.json")

        get_books(url="https://1lib.pl/s/javascript",
                  url_params={"yearFrom": 2022, "yearTo": 2022,
                              "languages%5B%5D": "english", "page": 1},
                  num_of_pages=10,
                  save_as_json="scrapped_pages/javascript.json")

        # get_download_links("scrapped_pages/django.json")

    except Exception as error:
        print(error)
