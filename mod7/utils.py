import logging_tree

from mod6.bank_with_logging import logger

with open('logging_tree.txt', 'w') as file:
    file.write(logging_tree.format.build_description())


class InvalidIndexOperation(Exception):
    def __init__(self):
        self.message = 'Invalid operation index entered'

    def __str__(self):
        return self.message


def get_number(mes=''):
    logger.debug('Start function "get_number"')
    while True:
        try:
            logger.info(mes)
            number = int(input())
            logger.debug('Return result from a function "get_number"')
            return number
        except ValueError as ex:
            logger.error(f'Invalid number\n{ex}')


def get_operation(mes=''):
    logger.debug('Start function "get_operation"')
    while True:
        try:
            logger.info(mes)
            index_operation = int(input())
            if 1 <= index_operation <= 3:
                logger.debug('Return result from a function "get_operation"')
                return index_operation
            raise InvalidIndexOperation()
        except ValueError as ex:
            logger.error(f'Invalid number\n{ex}')
        except InvalidIndexOperation as ex:
            logger.error(f'Invalid index operation\n{ex}')


def amount(n1, n2):
    logger.debug('Start function "amount"')
    return n1 + n2


def composition(n1, n2):
    logger.debug('Start function "composition"')
    return n1 * n2


def degree(n1, n2):
    logger.debug('Start function "degree"')
    return n1 ** n2
