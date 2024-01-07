# Generic imports
import logging

# Package Imports
from pynted.utils.requester import Requester
import pynted.exceptions.vinted as exceptions


logger: logging.Logger = logging.getLogger(__package__)


class Pynted():
    def __init__(self, login, password) -> None:
        self._email = login
        self._password = password
        self.requester = Requester()
        self._token = self.get_public_token()
        self.requester.headers.update({
            "Authorization": f"Bearer {self._token}"
        })


    def get_public_token(self):
        logger.info("Getting token")
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
        self._token = res.json()["access_token"]
        return res


    def login(self):
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
