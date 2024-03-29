# Generic imports
import logging
from typing import Dict

import pynted.exceptions.requester as req_exceptions
import pynted.exceptions.vinted as vin_exceptions

# Package Imports
from pynted.utils.requester import Requester
from pynted.vinted.user import VintedUser

logger: logging.Logger = logging.getLogger(__package__)


class Pynted:
    """Pynted class to interact with the vinted api.

    # Args:
        `locale` (str, optional): The locale to use. Defaults to "en".

    # Methods:
        Public:

            `get_user_by_username`: Get a user by its username.
            `get_brand`: Get a brand by its name.
            `search_item`: Search for an item on vinted.
        Private:
            `_retrieve_filters`: Get filters from the vinted api.
            `_get_public_token`: Retrieve the public `_token`
                and set it to the `Requester`.
    # Variables:
        Public:
            `filters`: The filters retrieved from the vinted api.
            `requester`: The requester class to make requests
                to the vinted api.
            `locale`: The locale to use.
            `base_url`: The base url of the vinted api.
            `colors`: The colors retrieved from the vinted api.
            `statuses`: The product statuses retrieved from the vinted api.
            `materials`: The materials retrieved from the vinted api.

        Private:
            `_token`: The token to use for the requests.
    # Raises:
        `req_exceptions.TooManyAttempts`: Too many attempts to to the server.
        `req_exceptions.InvalidCredentials`: Invalid credentials.
        `req_exceptions.UnknownError`: Unknown error occured during a request.
        `vin_exceptions.NoFilterRetrieved`: No filters retrieved from vynted.

    """

    def __init__(self, locale: str = "en") -> None:
        self.requester = Requester(locale)
        self.locale = locale
        self.base_url = "https://www.vinted.fr"
        self._token = None

        self._get_public_token()
        endpoint = f"{self.base_url}/api/v2/session_locale"
        self.requester.put(endpoint, data={"locale": "es-fr"})
        self.requester.headers.update({"Authorization": f"Bearer {self._token}"})
        self.colors: Dict = None
        self.statuses: Dict = None
        self.materials: Dict = None
        self._retrieve_filters()

    @property
    def filters(self) -> dict:
        """Filters retrieved from the vinted api.
        Returns:
            dict: {
                'colors': {color_name: color_id},
                'statuses': {status_name: status_id},
                'materials': {material_name: material_id}
            }
        """
        return {
            "colors": self.colors,
            "statuses": self.statuses,
            "materials": self.materials,
        }

    def get_user_by_username(self, username: str) -> VintedUser:
        """Get a user by its username.

        Args:
            username (str): The username of the user.

        Raises:
            * exceptions.UserNotFound: Raised when the user is not found.

        Returns:
            VintedUser: Vinted user class.
        """
        logger.debug("Getting user by username %s", username)
        endpoint = f"{self.base_url}/api/v2/users/{username}"
        res = self.requester.get(endpoint)
        if res.status_code == 404:
            raise vin_exceptions.UserNotFound(username=username)
        return VintedUser(res.json())

    def get_brand(self, brand: str) -> int:
        """Get a brand by its name.

        Args:
            brand (str): The name of the brand.

        Raises:
            * exceptions.BrandNotFound: Raised when the brand is not found.

        Returns:
            int: The id of the brand.
        """
        logger.debug("Getting brand %s", brand)
        brand = brand.replace(" ", "%20")
        path = "api/v2/catalog/filters/search"
        params = f"filter_search_code=brand&filter_search_text={brand}"
        endpoint = f"{self.base_url}/{path}?{params}"
        res = self.requester.get(endpoint)
        if res.status_code != 200:
            raise req_exceptions.UnknownError()
        if res.json()["options"] == []:
            raise vin_exceptions.BrandNotFound(brand=brand)
        return res.json()["options"][0]["id"]

    # def search_item(
    #     self,
    #     page: int = 1,
    #     per_page: int = 96,
    #     price_from: int = 0,
    #     price_to: int = 100000,
    # )

    # -+-+-+-+-+-+- #
    #    Private    #
    # -+-+-+-+-+-+- #

    def _retrieve_filters(self):
        """Get filters from vinted api, then add them to the class.

        Raises:
            req_exceptions.UnknownError: _description_
            vin_exceptions.NoFilterRetrieved: _description_
        """

        logger.debug("Getting filters")
        endpoint = f"{self.base_url}/api/v2/catalog/filters"
        res = self.requester.get(endpoint)
        if res.json()["code"] != 0:
            raise req_exceptions.UnknownError()
        # Assign the filters to the class via variables
        colors = [f for f in res.json()["filters"] if f.get("type") == "color"]
        statuses = [f for f in res.json()["filters"] if f.get("type") == "status"]
        materials = [f for f in res.json()["filters"] if f.get("type") == "material"]
        sizes = [f for f in res.json()["filters"] if f.get("type") == "size"]
        # Check if there is any of the list that is empty
        if not all([colors, statuses, sizes, materials]):
            raise vin_exceptions.NoFilterRetrieved()
        self.colors = {color["title"]: color["id"] for color in colors[0]["options"]}
        self.statuses = {
            status["title"]: status["id"] for status in statuses[0]["options"]
        }
        self.materials = {
            material["title"]: material["id"] for material in materials[0]["options"]
        }

    def _get_public_token(self):
        """Retrieve the public `_token` and set it to the `Requester`.

        Raises:
            * exceptions.TooManyAttempts: Raised when the server has
                blocked the user for too many attempts.
            * exceptions.InvalidCredentials: Raised when the user
                credentials are invalid.
            * exceptions.UnknownError: Raised when the code is not 200

        Returns:
            `Nothing`
        """
        logger.debug("Getting token")
        endpoint = f"{self.base_url}/oauth/token"
        data = {"scope": "public", "client_id": "android", "grant_type": "password"}
        res = self.requester.post(endpoint, data=data)
        if res.status_code == 403:
            raise req_exceptions.TooManyAttempts()
        if res.status_code == 401:
            raise req_exceptions.InvalidCredentials()
        if res.status_code != 200:
            raise req_exceptions.UnknownError()
        logger.debug("Token: %s", res.json()["access_token"])
        self._token = res.json()["access_token"]


__all__ = ["Pynted"]
