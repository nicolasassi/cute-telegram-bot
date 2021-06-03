from requests import get
from src.config.settings import BASE_WIKIPEDIA_API_URL


class Wiki:
    def __init__(self):
        self.random_page_url = BASE_WIKIPEDIA_API_URL + "page/random/summary"
        print(self.random_page_url)

    def _get_random(self):
        r = get(self.random_page_url)
        resp = r.json()
        if resp != {}:
            return resp
        raise Exception("no results")

    def get_random_page_info(self):
        rand = self._get_random()
        return {
            "title": rand.get("displaytitle", ""),
            "url": rand.get("content_urls", {}).get("mobile", {}).get("page", ""),
            "extract": rand.get("extract")
        }
