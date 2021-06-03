from requests import get
from src.config.settings import BASE_CAT_API_URL, CAT_API_TOKEN


class Cat:
    def __init__(self):
        self.random_image_url = BASE_CAT_API_URL + "images/search"
        self.auth_header = {"x-api-key": CAT_API_TOKEN}

    def _get_random(self):
        r = get(self.random_image_url, headers=self.auth_header)
        resp = r.json()
        if len(resp) >= 1:
            return resp[0]
        raise Exception("no results")

    def get_random_url(self):
        rand = self._get_random()
        return rand["url"]
