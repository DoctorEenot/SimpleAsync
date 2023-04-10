import time
import Task


def sleep(ctx, seconds: int):
    '''
        Simpliest and naive way of implementing sleep
    '''
    start_sleep = time.time()

    while time.time() - start_sleep < seconds:
        yield Task.Continue()
