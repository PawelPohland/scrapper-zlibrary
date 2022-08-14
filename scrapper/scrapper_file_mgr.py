import json
import os


class ScrapperFileManager:
    def __init__(self):
        ...

    # saves to external file
    def save_to_file(self, path, content):
        try:
            with open(path, "w") as file:
                file.write(content)
        except IOError as error:
            print(f"File error: {error}")

    # loads json file
    def get_books_from_json_file(self, path):
        try:
            path = os.path.expanduser(path)
            if os.path.exists(path):
                with open(path, "rt") as file:
                    return json.load(file)
            else:
                raise FileNotFoundError(path)
        except IOError as error:
            print(f"File error: {error}")
