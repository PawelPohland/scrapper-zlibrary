import urllib.parse


class ScrapperUrlParams:
    extensions = ["azw", "azw3", "djv", "djvu", "epub",
                  "fb2", "lit", "mobi", "pdf", "rtf", "txt"]

    languages = ["english", "arabic", "azerbaijani", "bengali", "chinese", "french", "greek",
                 "georgian", "hindi", "spanish", "dutch", "indonesian", "japanese", "korean",
                 "malaysian", "german", "armenian", "pashto", "polish", "portuguese", "russian",
                 "serbian", "thai", "telugu", "turkish", "ukrainian", "urdu", "vietnamese", "italian"]

    order = ["popular",  # by most popular
             "bestmatch",  # by best match
             "date",  # by recently added
             "titleA",  # by title (ascending)
             "title",  # by title (descending)
             "year",  # by year
             "filesize",  # by file size (descending)
             "filesizeA"  # by file size (ascending)
             ]

    def __init__(self, base_url, search_term=None, year_from=None, year_to=None, languages=None, extensions=None, order=None):
        self.base_url = base_url if not base_url.endswith(
            "/") else base_url[0:-1:]

        self.search_term = search_term
        self.year_from = year_from
        self.year_to = year_to

        self.languages = languages
        self.extensions = extensions

        self.order = order

    def get_url_params(self):
        url_params = []

        if self.year_from:
            url_params.append(f"yearFrom={self.year_from}")

        if self.year_to:
            url_params.append(f"yearTo={self.year_to}")

        if self.languages and len(self.languages):
            for lang in self.languages:
                if lang in ScrapperUrlParams.languages:
                    url_params.append(
                        f"{urllib.parse.quote('languages[]')}={lang}")

        if self.extensions and len(self.extensions):
            for ext in self.extensions:
                if ext in ScrapperUrlParams.extensions:
                    url_params.append(
                        f"{urllib.parse.quote('extensions[]')}={ext}")

        if self.order in ScrapperUrlParams.order:
            url_params.append(f"order={self.order}")

        if len(url_params):
            return "&".join(url_params)

    def get_full_url(self):
        full_url = f"{self.base_url}/s/"

        if self.search_term:
            full_url += urllib.parse.quote(self.search_term)

        url_params = self.get_url_params()

        if url_params:
            full_url += f"?{url_params}"

        return full_url
