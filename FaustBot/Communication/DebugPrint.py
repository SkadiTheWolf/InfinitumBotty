__author__ = "Daniela"

from FaustBot import logger


class DebugPrint(object):
    def print(self, message):
        """
        :param message: What to print to debug output
        :return:
        """
        logger.debug(message)
