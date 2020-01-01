''' test limited_as_completed
'''
from pathlib import Path
import sys
import asyncio

# import pytest
from loguru import logger

BASE_DIR = Path(__file__).absolute().parent.parent.as_posix()
CUR_DIR = Path(__file__).absolute().parent.as_posix()

# sys.path.append(BASE_DIR)

# from jhao.ProxyGetter import getFreeProxy

# pylint: disable=wrong-import-position, import-error  # noqa
from simple_pp.limited_as_completed import limited_as_completed
from simple_pp.aio_headers import timed_fetch_headers
# from simple_pp.simple_pp import simple_pp


def test_as_completed_afunc_bfunc():
    ''' test limited as completed'''

    _ = '''
    assert hasattr(getFreeProxy, 'GetFreeProxy')

    res = [*getFreeProxy.GetFreeProxy.freeProxy01()]
    # print('print res:', res)
    logger.debug(f'res: {res}')
    assert res
    # '''

    async def afun(xarg=1):
        await asyncio.sleep(0)
        return xarg

    async def bfun(xarg=2):
        asyncio.sleep(0)  # ought to generate a warning in pytest py3.7
        # RuntimeWarning: coroutine 'sleep' was never awaited

        return -xarg

    coros = iter([afun(), bfun(), afun(), bfun(), ])
    res = [*limited_as_completed(coros)]
    logger.debug(res)
    assert sum(res) == -2


def test_res_info_pkl():
    ''' test res_info.pkl '''
    import pickle
    from pprint import pprint
    from tqdm import tqdm

    from timeme import timeme

    _ = '''
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = get_new_loop()
        asyncio.set_event_loop(loop)
    # '''

    logger.remove()
    logger.add(sys.stderr, level='INFO')

    repeat = 1

    pklfile = Path(CUR_DIR, 'res_info.pkl')
    logger.debug(f'pklfile: {pklfile}')
    res_info = pickle.load(open(pklfile, 'rb'))

    coros = (timed_fetch_headers(elm) for elm in res_info * repeat)

    limit = 270  # 25 s
    limit = 30  #  45-60.227s

    res = []

    with timeme():
        for idx, elm in enumerate(tqdm(limited_as_completed(coros, limit=limit))):
            res.append(elm)

    # res = [*limited_as_completed(coros, limit=limit)]

    # logger.info(res)
    pprint([res, len(res)])

    assert res
