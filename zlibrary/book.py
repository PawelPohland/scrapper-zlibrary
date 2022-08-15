class Book:
    base_url = "https://1lib.pl"

    def __init__(self, parser=None):
        self.parser = parser

        self.id = ""
        self.isbn = ""
        self.title = ""

        self.url = ""
        self.cover = ""

        self.year = ""
        self.language = ""

        self.authors = []
        self.publisher = ""

        self.files_types = []

    def parse_id(self):
        self.id = self.parser.get("data-book_id", "")

    def parse_isbn(self):
        isbn = self.parser.select_one("[data-isbn]")
        if isbn:
            self.isbn = isbn.get("data-isbn", "")

    def parse_title(self):
        link = self.parser.select_one('[itemprop="name"] > a')

        self.title = link.string
        self.url = f"{self.base_url}{link.get('href', '')}"

    def get_bigger_img(self, image):
        imgs = image.get("data-srcset", "").split(",")
        images = []

        for img in imgs:
            images.append(img.split()[0])

        return images[-1]

    def parse_cover(self):
        image = self.parser.select_one(".itemCover img")
        if image:
            #self.cover = self.get_bigger_img(image)
            self.cover = image.get("data-src", "")

    def parse_authors(self):
        authors = self.parser.select('[itemprop="author"]')
        if authors:
            for author in authors:
                if author.string:
                    self.authors.append(author.string)

    def parse_publisher(self):
        pub = self.parser.select_one('a[title="Publisher"]')
        if pub:
            self.publisher = pub.string

    def parse_year(self):
        year = self.parser.select_one(".property_year > .property_value")
        if year:
            self.year = year.string

    def parse_language(self):
        lang = self.parser.select_one(".property_language > .property_value")
        if lang:
            self.language = lang.string

    def parse_files(self):
        file_type = self.parser.select_one(".property__file > .property_value")
        if file_type:
            file_type = file_type.string.split(",")
            ft = {
                "file_type": file_type[0],
                "file_size": file_type[1].lstrip(),
                "url": self.url
            }

            self.files_types.append(ft)

    def parse(self):
        self.parse_id()
        self.parse_isbn()
        self.parse_title()
        self.parse_cover()
        self.parse_authors()
        self.parse_publisher()
        self.parse_year()
        self.parse_language()
        self.parse_files()

    def add_file(self, other_book):
        if not self.isbn:
            self.isbn = other_book.isbn

        self.files_types.extend(other_book.files_types)

    def print(self):
        print("*" * 50)
        print(f"ID: {self.id}")
        print(f"ISBN: {self.isbn}")
        print(f"Title: {self.title}")
        print(f"Url: {self.url}")
        print(f"Cover: {self.cover}")
        print(f"Year: {self.year}")
        print(f"Language: {self.language}")
        print(f"Author(s): {', '.join(self.authors)}")
        print(f"Publisher: {self.publisher}")
        print(f"Files: {self.files_types}")

    def __str__(self):
        return f"<class 'Book'>"

    def __del__(self):
        del self.parser

    def compare_authors(self, other_book):
        if len(self.authors) == len(other_book.authors):
            counter = 0
            the_same = 0
            for self_author, other_author in zip(self.authors, other_book.authors):
                if self_author.lower() == other_author.lower():
                    the_same += 1
                counter += 1

            if counter == 0:
                return False

            # if at least 60% of authors are the same
            if the_same / counter >= 0.6:
                return True

        return False

    # compare books
    def __eq__(self, other_book):
        # if isbn is set and equal - assume that books are the same
        if self.isbn and self.isbn == other_book.isbn:
            return True

        # if both books have different isbn - assume different books
        if self.isbn and other_book.isbn:
            return False

        # otherwise - check other properties and use equality weight
        eq_weight = 0

        if self.title and self.title.lower() == other_book.title.lower():
            eq_weight += 1

        if self.year and self.year == other_book.year:
            eq_weight += 1

        if self.language and self.language.lower() == other_book.language.lower():
            eq_weight += 1

        if self.publisher and self.publisher.lower() == other_book.publisher.lower():
            eq_weight += 1

        if self.compare_authors(other_book):
            eq_weight += 1

        # number of properties that was compared
        # (title, year, language, publisher, authors)
        properties = 5

        # percentage equality
        eq_percentage = 100 * eq_weight / properties

        # if majority of book's properties, say 60% (so at least 3 properties),
        # have the same value - assume that books are the same
        if eq_percentage >= 60:
            return True

        return False

    # returns dictionary object with books properties
    def serialize(self):
        return {
            "id": self.id,
            "isbn": self.isbn,
            "title": self.title,
            "url": self.url,
            "cover": self.cover,
            "year": self.year,
            "language": self.language,
            "authors": [author for author in self.authors],
            "publisher": self.publisher,
            "files_types": [ft for ft in self.files_types]
        }

    # loads data from dictionary object (loaded from json file)
    def deserialize(self, book_dict):
        self.id = book_dict.get("id", "")
        self.isbn = book_dict.get("isbn", "")
        self.title = book_dict.get("title", "")
        self.url = book_dict.get("url", "")
        self.cover = book_dict.get("cover", "")
        self.year = book_dict.get("year", "")
        self.language = book_dict.get("language", "")
        self.authors = book_dict.get("authors", [])
        self.publisher = book_dict.get("publisher", "")
        self.files_types = book_dict.get("files_types", [])
