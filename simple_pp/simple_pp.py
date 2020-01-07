'''
simple proxy pool
'''
# pyright: strict

from typing import (Union, List, Tuple, Any, Generator)

import re

from .timeme import timeme  # tpye: ignore
from .limited_as_completed import limited_as_completed
from .aio_headers import timed_fetch_headers
from .need_to_wrap import need_to_wrap

# from collections import deque
# PROXYPOOL = deque()


def simple_pp(
        proxies: Union[str, List[Any], Tuple[Any, ...]],
        timeout: float = 4,
) -> List[Any]:
    ''' simeple proxy pool '''

    # (\d{1,3}(?:\.\d{1,3}){3})(?:[:\s]+(\d{1,5})(?=[^\d\.]))?
    # (\d{1,3}(?:\.\d{1,3}){3})(?:[^\d\.]+(\d{1,5})(?=[^\d\.]))?

    patt = re.compile(r'(?:https?://)?(\d{1,3}(?:\.\d{1,3}){3})(?:[\s\t:\'",]+(\d{1,4}))?')
    if isinstance(proxies, str):
        # _ = re.findall(r'(?:https?://)?[\d\.]{8,16}(?::\d{1,4})?', proxies)
        _ = [':'.join(elm) if elm[1] else elm[0] for elm in patt.findall(proxies)]
        proxies = tuple(_)

    if need_to_wrap(proxies):
        proxies = (proxies,)

    coros = (timed_fetch_headers(proxy, timeout=timeout) for proxy in proxies)
    # Generator  # pyright: ignore

    with timeme():
        res = [*limited_as_completed(coros)]  # type: list

    return res
