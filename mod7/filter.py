import logging


class Filter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return str.isascii(record.message)
