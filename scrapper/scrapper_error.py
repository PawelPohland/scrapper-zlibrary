class ScrapperError(Exception):
    def __init__(self, message, *args):
        super().__init__(args)
        self.message = message

    def __str__(self):
        return f"~ Scrapper Error: {self.message}"
