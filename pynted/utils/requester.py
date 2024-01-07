import logging
import requests
import json
logger: logging.Logger = logging.getLogger(__package__)


class Requester():
    """Requester class to make generic requests to the vinted api.
        This is not the main class to request to vinted, it's just making requests.
        It needs to store cookies, headers, and other stuff to make requests.
    """
    def __init__(self):
        self.headers = {}
        self.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        })

    def post(self, endpoint: str, data: dict = {})-> requests.Response:
        logger.debug("POST request to %s with params %s", endpoint, data)
        try:
            res = requests.post(
                endpoint,
                params=json.dumps(data),
                headers=self.headers
            )
            return res
        except requests.exceptions.Timeout:
            logger.error("Request timed out for %s", endpoint)
            return None
        except requests.exceptions.ConnectionError:
            logger.error("Connection error for %s", endpoint)
            return None
