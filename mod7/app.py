from utils import *
import logging.config
from config import config_logging


logging.config.dictConfig(config_logging)
logger = logging.getLogger('calculate_logger')


def calculate():
    logger.info('Start calculate')
    logger.debug('Data request')
    num1 = get_number('Введите первое число: ')
    num2 = get_number('Введите второе число: ')
    operation = get_operation('Выберете операцию:\n1. Сложение\n2. Произведение\n3. Возведение в степень\n')
    logger.debug('Data received')
    result = 0
    if operation == 1:
        result = amount(num1, num2)
        operation = '+'
    elif operation == 2:
        result = composition(num1, num2)
        operation = '*'
    elif operation == 3:
        result = degree(num1, num2)
        operation = '^'
    logger.info(f'{num1} {operation} {num2} = {result}')
    logger.debug('Print result of operation')


if __name__ == '__main__':
    calculate()
