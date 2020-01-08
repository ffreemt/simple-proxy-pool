'''
example use: async-headers.py:
    coros = iter([async_func()...])
    res = [*limited_as_completed(coros, limit=limit)]

https://artificialworlds.net/presentations/python-async/python-async.html x

https://www.artificialworlds.net/blog/2017/06/12/making-100-million-requests-with-python-aiohttp/
'''
# pyright: strict

from typing import Union, Generator, Iterator, List, Tuple, Any

import asyncio
from itertools import islice


def limited_as_completed(coros: Union[Generator, Iterator], limit: float = 30) -> Generator:
    ''' limited_as_completed '''
    loop = asyncio.get_event_loop()
    if loop.is_closed():  # pragma: no cover
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    futures = [
        asyncio.ensure_future(_)
        for _ in islice(coros, 0, limit)  # type: ignore
    ]

    async def first_to_finish():
        while True:
            await asyncio.sleep(0)
            for fut in futures:
                if fut.done():
                    futures.remove(fut)
                    try:
                        newf = next(coros)
                        futures.append(
                            asyncio.ensure_future(newf))
                    except StopIteration as _:
                        pass
                    return fut.result()
    # while len(futures) > 0:
    while futures:
        # elm =
        # yield elm
        yield loop.run_until_complete(first_to_finish())
