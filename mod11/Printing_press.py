import logging
import random
import threading
import time

TOTAL_TICKETS = 10
PRINTING_THRESHOLD = 4

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore, printing_event: threading.Event):
        super().__init__()
        self.sem = semaphore
        self.printing_event = printing_event
        logger.info('Director started work')

    def run(self):
        while True:
            self.printing_event.wait()
            with self.sem:
                global TOTAL_TICKETS
                if TOTAL_TICKETS <= 0:
                    break
                additional_tickets = random.randint(1, 6)
                TOTAL_TICKETS += additional_tickets
                logger.info(f'Director printed {additional_tickets} additional tickets; {TOTAL_TICKETS} total')
                self.printing_event.clear()

        logger.info('Director finished printing tickets')


class Seller(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore, printing_event: threading.Event):
        super().__init__()
        self.sem = semaphore
        self.printing_event = printing_event
        self.tickets_sold = 0
        logger.info('Seller started work')

    def run(self):
        global TOTAL_TICKETS
        is_running = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.getName()} sold one; {TOTAL_TICKETS} left')
                if TOTAL_TICKETS == PRINTING_THRESHOLD:
                    self.printing_event.set()

        logger.info(f'Seller {self.getName()} sold {self.tickets_sold} tickets')

    def random_sleep(self):
        time.sleep(random.randint(0, 1))


def main():
    semaphore = threading.Semaphore()
    printing_event = threading.Event()
    sellers = []

    for _ in range(3):
        seller = Seller(semaphore, printing_event)
        seller.start()
        sellers.append(seller)

    director = Director(semaphore, printing_event)
    director.start()

    for seller in sellers:
        seller.join()

    director.join()


if __name__ == '__main__':
    main()