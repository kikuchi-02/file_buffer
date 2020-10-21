import fcntl
import time
import os

from functools import wraps
from time import sleep

buffer_file = 'main.buffer'
max_size = 100


def coroutine(f):
    @wraps(f)
    def primer(*args, **kwargs):
        g = f(*args, **kwargs)
        next(g)
        return g

    return primer


def task(file_name):
    sleep(3)
    os.remove(file_name)


@coroutine
def file_buffer():
    """file buffer

    usage:
        receiver = file_buffer()
        receiver.send('hell')
    """
    while True:
        value = yield
        with open(buffer_file, 'a') as f:
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                time.sleep(0.2)
                continue

            if not os.path.isfile(buffer_file):
                continue

            print(value, file=f)
            if os.path.getsize(buffer_file) > max_size:
                sub_file = 'sub.buffer'
                os.rename(buffer_file, sub_file)
                task(sub_file)

            fcntl.flock(f, fcntl.LOCK_UN)
