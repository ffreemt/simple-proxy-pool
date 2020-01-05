'''
quick httpx.get
'''

from asyncio import get_event_loop, new_event_loop, set_event_loop
import httpx


def httpx_get(*args, **kwargs):
    ''' quick httpx.get

    >>> httpx_get('http://httpbin.org/user-agent').json()['user-agent'][:6]
    'python'
    >>> httpx_get('http://httpbin.org/user-agent', headers={'User-Agent': 'xxx'}).json()['user-agent']
    'xxx'
    '''
    loop = get_event_loop()
    if loop.is_closed():  # pragma: no cover
        loop = new_event_loop()
        set_event_loop(loop)
    return loop.run_until_complete(httpx.get(*args, **kwargs))
