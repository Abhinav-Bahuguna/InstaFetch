
import random
import time


def random_sleep(min, max):
    random_number = random.randint(min, max)
    time.sleep(random_number)
