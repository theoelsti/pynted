import json
import logging

import requests

logger: logging.Logger = logging.getLogger(__package__)


class Requester:
    """Requester class to make generic requests to the vinted api.
    This class is just making requests.
    It needs to store cookies, headers, and other stuff to make requests.
    """

    def __init__(self, locale):
        if locale != "fr":
            locale = f"{locale}-fr"
        self.session = requests.Session()
        self.headers = {}
        self.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) "
                    "Gecko/20100101 Firefox/121.0"
                ),
                "Content-Type": "application/json; charset=UTF-8",
                "Cookie": f"locale={locale};",
            }
        )

    def post(self, endpoint: str, data: dict = None) -> requests.Response:
        """Post request to the vinted api.

        Args:
            endpoint (str): Endpoint to make the request to.
            data (dict, optional): Data for the request. Defaults to None.

        Returns:
            requests.Response: Request class from the requests library.
        """
        if data is None:
            data = {}
        logger.debug("POST request to %s with params %s", endpoint, data)
        try:
            res = self.session.post(
                endpoint, data=json.dumps(data), headers=self.headers
            )
            return res
        except requests.exceptions.Timeout:
            logger.error("Request timed out for %s", endpoint)
            return None
        except requests.exceptions.ConnectionError:
            logger.error("Connection error for %s", endpoint)
            return None

    def get(self, endpoint: str, params: dict = None) -> requests.Response:
        """GET request to the vinted api.

        Args:
            `endpoint` (str): The endpoint to make the request to.
            `params` (dict, optional): Params added to the request.

        Returns:
            `requests.Response`: _description_
        """
        if params is None:
            params = {}
        logger.debug("GET request to %s with params %s", endpoint, params)
        try:
            res = self.session.get(endpoint, params=params, headers=self.headers)
            return res
        except requests.exceptions.Timeout:
            logger.error("Request timed out for %s", endpoint)
            return None
        except requests.exceptions.ConnectionError:
            logger.error("Connection error for %s", endpoint)
            return None

    def put(self, endpoint: str, data: dict = None) -> requests.Response:
        """PUT request to the vinted api.

        Args:
            endpoint (str): The endpoint to make the request to.
            data (dict, optional): Data for the request. Defaults to None.

        Returns:
            requests.Response: Request class from the requests library.
        """
        if data is None:
            data = {}
        logger.debug("PUT request to %s with params %s", endpoint, data)
        try:
            res = self.session.put(endpoint, data=data, headers=self.headers)
            return res
        except requests.exceptions.Timeout:
            logger.error("Request timed out for %s", endpoint)
            return None
        except requests.exceptions.ConnectionError:
            logger.error("Connection error for %s", endpoint)
            return None
