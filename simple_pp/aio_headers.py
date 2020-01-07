r'''
simple proxy pool/validator based on aiohttp, fast

some of the ProxyGetter functions are from jhao's proxy_pool porject

based on async-headers.py in playground\simple_proxypool
example use:
    coros = (async_func()...)  [generator or iterator]
    res = [*limited_as_completed(coros, limit=limit)]
'''
from typing import List, Union, Any

import sys
from timeit import default_timer
import asyncio
import aiohttp
from aiohttp import ClientSession
from multidict import CIMultiDict

from async_timeout import timeout as atimeout
from tqdm import tqdm  # type: ignore

from loguru import logger

from .make_url import make_url
from .timeme import timeme
from .get_new_loop import get_new_loop
asyncio.set_event_loop(get_new_loop())

# session = ClientSession()
SEM = asyncio.Semaphore(1000)


async def fetch_headers(url, session=None, proxy=None):
    '''  fetch_headers from www.baidu.com via a proxy


    :return: reached baidu, ano '''

    # obtain a session when session is None or closed
    if session is None or isinstance(session, aiohttp.client.ClientSession) and session.closed:  # noqa
        session = ClientSession()

    if asyncio.get_event_loop().is_closed():
        asyncio.set_event_loop(get_new_loop())
    fetch_headers.headers = CIMultiDict(fetch='')

    reached_bd, via = None, False
    async with session.get(url, proxy=proxy) as response:
        fetch_headers.headers = response.headers
        via = response.headers.get("via")
        # date = response.headers.get("DATE")
        set_cookie = ' '.join(response.headers.getall("Set-Cookie", 'none'))
        # bdqid = response.headers.get("Bdqid")
        # print("{}:{} with via [{}] full headers:\n\t{}".format(date, response.url, delay, response.headers))
        # print("{}: {} with via: \n\t[{}] \n'Set-Cookie':\n\t{}".format(date, response.url, via, set_cookie))
        fetch_headers.headers = response.headers

    # return (reached baidu, ano)
    reached_bd = 'domain=.baidu.com' in set_cookie
    return reached_bd, reached_bd and not via,


async def bound_fetch_headers(sem, url, session, proxy):
    ''' bound (by = asyncio.Semaphore(1000)) fetch_headers '''
    if asyncio.get_event_loop().is_closed():
        asyncio.set_event_loop(get_new_loop())

    # Getter function with semaphore
    bound_fetch_headers.headers = CIMultiDict(bound_fetch='')
    async with SEM:
        _ = await fetch_headers(url, session, proxy)
        bound_fetch_headers.headers = fetch_headers.headers
        return _


# async def simple_pp(
# async def timed_fetch_headers(proxy, timeout_=4):
async def timed_fetch_headers(
        proxy: Union[tuple, list, str],
        timeout: float = 4,
) -> Union[tuple, list, str]:
    ''' time restricted (default 4 s) of bound_fetch_headers

    :return: reached baidu, ano '''
    if isinstance(proxy, str):
        proxy_ = tuple([proxy])

    if isinstance(proxy, list):
        proxy_ = tuple(proxy[:])
        proxy = proxy_[0]
    else:
        if isinstance(proxy, tuple):
            proxy_ = proxy[:]
            proxy = proxy_[0]

    async with ClientSession() as session:
        try:
            proxy = make_url(proxy)
        except Exception as exc:
            logger.warning('make_url exc: %s' % exc)

        then = default_timer()
        try:
            async with atimeout(timeout) as t:
                try:
                    # _ = await fetch_headers('http://www.baidu.com'.format(0), session, make_url(proxy))
                    # await fetch('http://www.baidu.com'.format(0), session, make_url(proxy))
                    # _ = await bound_fetch_headers(SEM, 'http://www.baidu.com', session, make_url(proxy))
                    _ = await bound_fetch_headers(SEM, 'http://www.baidu.com', session, proxy)
                except Exception as exc:
                    logger.debug(' fetch_headers exc: %s ' % exc)
                    _ = str(exc), False

                elapsed_time = round(default_timer() - then, 2)
                # return _, elapsed_time
                return proxy_ + _ + (elapsed_time, )

        except Exception as exc:
            logger.info(' TimeoutError exc: %s ' % exc)
            return str(exc)


def main():
    ''' main '''
    # import


if __name__ == '__main__':
    main()
