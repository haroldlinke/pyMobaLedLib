"""Logging infrastructure"""

import logging
import fnmatch
from .config import VB2PYConfig

Config = VB2PYConfig()


class VB2PYLogger(logging.StreamHandler):
    """Logger which can do some interesting filtering"""

    allowed = []  # Loggers which can report
    blocked = []  # Loggers which can't report

    def filter(self, record):
        """Filter logging events"""
        for allow in self.allowed:
            if fnmatch.fnmatch(record.name, allow) and record.name not in self.blocked:
                # print('filtering yes', record.name)
                return 1
        # print('filtering no "%s", allow %s, block %s' % (record.name, self.allowed, self.blocked))

    def initConfiguration(self, conf):
        """Initialize the configuration"""
        self.allowed = self._makeList(conf["Logging", "Allowed"])
        self.blocked = self._makeList(conf["Logging", "NotAllowed"])

    @staticmethod
    def _makeList(text):
        """Make a list from a comma separated list of names"""
        names = text.split(",")
        return [name.strip() for name in names]


main_handler = VB2PYLogger()
main_handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
main_handler.initConfiguration(Config)


def getLogger(name, level=None):
    """Create a logger with the usual settings"""
    if level is None:
        level = int(Config["General", "LoggingLevel"])
    log = logging.getLogger(name)
    log.addHandler(main_handler)
    log.setLevel(level)
    return log
