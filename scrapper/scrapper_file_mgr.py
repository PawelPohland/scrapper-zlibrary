from jinja2 import Environment
from jinja2 import FileSystemLoader

import time
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

    # saves html file
    def render_html_template(self, path, page_title, books):
        template_file_loader = FileSystemLoader("scrapper")
        env = Environment(loader=template_file_loader)
        template = env.get_template("template.html")

        time_gen = time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())

        output = template.render(
            page_title=page_title, generated_at=time_gen, books=books)

        self.save_to_file(path, output)

    def get_cwd_full_path(self, file=None):
        fullpath = f"{os.getcwd()}{os.sep}"

        if file:
            fullpath += file

        return fullpath
