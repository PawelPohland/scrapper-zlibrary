class Book:
    base_url = "https://1lib.pl"

    def __init__(self):
        self.isbn = ""
        self.title = ""

        self.url = ""
        self.cover = ""

        self.year = ""
        self.language = ""

        self.authors = []
        self.publisher = ""

        self.files_types = []
        self.links = []

    def parse_isbn(self, parser):
        isbn = parser.select_one("[data-isbn]")
        if isbn:
            self.isbn = isbn.get("data-isbn")

    def parse_title(self, parser):
        link = parser.select_one('[itemprop="name"] > a')

        self.title = link.string
        self.url = f"{self.base_url}{link.get('href')}"

    def parse_cover(self, parser):
        image = parser.select_one(".itemCover img")
        if image:
            # imgs = image.get("data-srcset").split(",")
            # images = []

            # for img in imgs:
            #     images.append(img.split()[0])

            # self.cover = images[-1]

            self.cover = image.get("data-src")

    def parse_authors(self, parser):
        authors = parser.select('[itemprop="author"]')
        if authors:
            for author in authors:
                self.authors.append(author.string)

    def parse_publisher(self, parser):
        pub = parser.select_one('a[title="Publisher"]')
        if pub:
            self.publisher = pub.string

    def parse_year(self, parser):
        year = parser.select_one(".property_year > .property_value")
        if year:
            self.year = year.string

    def parse_language(self, parser):
        lang = parser.select_one(".property_language > .property_value")
        if lang:
            self.language = lang.string

    def parse_files(self, parser):
        file_type = parser.select_one(".property__file > .property_value")
        if file_type:
            file_type = file_type.string.split(",")
            ft = {
                "file_type": file_type[0],
                "file_size": file_type[1].lstrip(),
                "url": self.url
            }

            self.files_types.append(ft)

    def parse(self, parser):
        self.parse_isbn(parser)
        self.parse_title(parser)
        self.parse_cover(parser)
        self.parse_authors(parser)
        self.parse_publisher(parser)
        self.parse_year(parser)
        self.parse_language(parser)
        self.parse_files(parser)

    def print(self):
        print("*" * 30)
        print(f"ISBN: {self.isbn}")
        print(f"Title: {self.title}")
        print(f"Cover: {self.cover}")
        print(f"Author(s): {', '.join(self.authors)}")
        print(f"Publisher: {self.publisher}")
        print(f"Year: {self.year}")
        print(f"Language: {self.language}")
        print(f"Files: {self.files_types}")

    def __str__(self):
        return f"<class 'Book'>"
