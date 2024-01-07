# Generic imports
import logging

# Package Imports
from pynted.utils.requester import Requester
import pynted.exceptions.requester as exceptions


logger: logging.Logger = logging.getLogger(__package__)


class Pynted():
    def __init__(self) -> None:
        self.requester = Requester()
        self._token = None
        self.get_public_token()
        self.requester.headers.update({
            "Authorization": f"Bearer {self._token}"
        })


    def get_public_token(self):
        """Retrieve the public `_token` and set it to the `Requester`.

        Raises:
            * exceptions.TooManyAttempts: Raised when the server has blocked the user for too many attempts.
            * exceptions.InvalidCredentials: Raised when the user credentials are invalid.
            * exceptions.UnknownError: Raised when the code is not 200

        Returns:
            `Nothing`
        """
        logger.debug("Getting token")
        endpoint = "https://www.vinted.fr/oauth/token"
        data = {
            "scope": "public",
            "client_id": "android",
            "grant_type": "password"
        }
        res = self.requester.post(
            endpoint,
            data = data
        )
        if res.status_code == 403:
            raise exceptions.TooManyAttempts()
        if res.status_code == 401:
            raise exceptions.InvalidCredentials()
        if res.status_code != 200:
            raise exceptions.UnknownError()
        logger.debug("Token: %s", res.json()["access_token"])
        self._token = res.json()["access_token"]


    def login(self, user, password):
        logger.info("Logging in")
        endpoint = "https://www.vinted.fr/api/v2/users?adjust_campaign=Organic"
        data = {
            "user": {
                "agree_rules": True,
                "login": self._email,
                "password": self._password,
                "user_settings": {
                    "is_newsletter_subscriber": False,
                }
            }
        }
        res = self.requester.post(
            endpoint,
            data = data
        )
        if res.status_code == 401:
            raise exceptions.InvalidCredentials()
        if res.status_code == 403:
            raise exceptions.TooManyAttempts()
        return res
