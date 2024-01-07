import logging
from pynted.vinted import Pynted
logger: logging.Logger = logging.getLogger(__package__)


def main():
    logger.info("Reaching main function")
    vinted = Pynted("theophile.fouillet@gmail.com", "A3=Ga[jA]")
