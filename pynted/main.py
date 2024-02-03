import logging

import pynted.exceptions.requester as req_exceptions
from pynted.vinted import Pynted

logger: logging.Logger = logging.getLogger(__package__)


def main():
    logger.info("Reaching main function")
    try : 
        vinted = Pynted()
    except req_exceptions.InvalidCredentials:
        logger.error("Invalid credentials")
        return
    except req_exceptions.TooManyAttempts:
        logger.error("Too many attempts")
        return
    except req_exceptions.UnknownError:
        logger.error("Unknown error")
        return
