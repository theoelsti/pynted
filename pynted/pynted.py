# Generic imports
import logging

# Package Imports
from pynted.utils.requester import Requester
import pynted.exceptions.requester as req_exceptions
import pynted.exceptions.vinted as vin_exceptions
from pynted.vinted.user import VintedUser

logger: logging.Logger = logging.getLogger(__package__)


class Pynted():
    def __init__(self) -> None:
        self.requester = Requester()
        self._token = None
        self.get_public_token()
        self.requester.headers.update({
            "Authorization": f"Bearer {self._token}"
        })

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
        endpoint = f"https://www.vinted.fr/api/v2/users/{username}"
        res = self.requester.get(endpoint)
        if res.status_code == 404:
            raise vin_exceptions.UserNotFound(username=username)
        return VintedUser(res.json())

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
            raise req_exceptions.TooManyAttempts()
        if res.status_code == 401:
            raise req_exceptions.InvalidCredentials()
        if res.status_code != 200:
            raise req_exceptions.UnknownError()
        logger.debug("Token: %s", res.json()["access_token"])
        self._token = res.json()["access_token"]
