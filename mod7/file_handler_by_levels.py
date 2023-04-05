import logging


class FileHandlerByLevels(logging.Handler):
    def __init__(self, mode='a'):
        super().__init__()
        self.mode = mode

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        with open(f'logs/calc_{record.levelname.lower()}.log', self.mode) as file:
            file.write(f'{message}\n')
