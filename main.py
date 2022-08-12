import scrapper


if __name__ == "__main__":
    try:
        scrapper = scrapper.Scrapper()
        # scrapper.get_books("https://1lib.pl/s/django?yearFrom=2022&yearTo=2022&languages%5B%5D=english")
        # scrapper.get_books("https://1lib.pl/s/django",
        #                    url_params={"yearFrom": 2022, "yearTo": 2022, "languages%5B%5D": "english", "page": 1})

        scrapper.get_books("https://1lib.pl/s/javascript",
                           url_params={"yearFrom": 2022, "yearTo": 2022, "languages%5B%5D": "english", "page": 1}, num_of_pages=10)
        scrapper.save_books_as_json("scrapped_pages/javascript.json")

    except Exception as error:
        print(error)
