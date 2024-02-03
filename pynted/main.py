import logging

from pynted.pynted import Pynted

logger: logging.Logger = logging.getLogger(__package__)


def main():
    logger.info("Reaching main function")
    vinted = Pynted()
    celine = vinted.get_brand('Celine')
    logger.info(celine)
    user = vinted.get_user_by_username('theofoui')
    logger.info(user)
