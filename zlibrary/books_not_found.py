class BooksNotFound(Exception):
    def __init__(self, url, url_params, *args):
        super().__init__(args)

        self.url = url
        self.url_params = url_params

    def __str__(self):
        return f"No books found at '{self.url}' [{self.url_params}]"
