''''report time
'''
from typing import Generator

import contextlib
from time import perf_counter

@contextlib.contextmanager
def timeme() -> Generator:
    then = perf_counter()  # type: float
    yield
    time_elapsed = float(f'{perf_counter() - then:.6f}')
    print("Time elapsed: %.3f s" % time_elapsed)
