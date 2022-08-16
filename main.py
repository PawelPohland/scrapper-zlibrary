import scrapper.scrapper as scrapper
from scrapper.scrapper_url_params import ScrapperUrlParams

import webbrowser


def load_books_from_json_file(path):
    scr = scrapper.Scrapper()
    scr.get_books_from_json(path)
    return scr


def get_download_links(path):
    scr = load_books_from_json_file(path)
    scr.get_books_download_links()
    scr.save_books_as_json(path)


def get_books(url, url_params=None, num_of_pages=1, start_from_page=1, save_as_json=None):
    scr = scrapper.Scrapper()
    scr.get_books(url, url_params, num_of_pages, start_from_page)

    if save_as_json:
        scr.save_books_as_json(save_as_json)

    return scr


def render_html_from_json_file(json_path, html_path, page_title, open_in_browser=False):
    scr = load_books_from_json_file(path=json_path)
    scr.save_books_as_html(file_path=html_path, page_title=page_title)

    if open_in_browser:
        fullpath = scr.file_mgr.get_cwd_full_path(file=html_path)
        webbrowser.open(url=f"file://{fullpath}", new=2)


def render_html_from_url(url_params, html_path, page_title, open_in_browser=False):
    scr = get_books(url=url_params.get_full_url(), url_params={},
                    num_of_pages=1, start_from_page=1, save_as_json=False)
    scr.save_books_as_html(file_path=html_path, page_title=page_title)

    if open_in_browser:
        fullpath = scr.file_mgr.get_cwd_full_path(file=html_path)
        webbrowser.open(url=f"file://{fullpath}", new=2)


if __name__ == "__main__":
    try:
        # render_html_from_json_file(json_path="scrapped_pages/django.json",
        #                            html_path="scrapped_pages/django.html",
        #                            page_title="Django books", open_in_browser=True)

        url_params = ScrapperUrlParams(base_url="https://1lib.pl", search_term="javascript", year_from=2022,
                                       year_to=2022, languages=["english", "polish"], extensions=["pdf"], order="date")
        render_html_from_url(url_params=url_params, html_path="scrapped_pages/javascript.html",
                             page_title="JavaScript books", open_in_browser=True)
    except Exception as error:
        print(error)
