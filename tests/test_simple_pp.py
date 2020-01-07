'''
various tests for simple_pp
'''
from pathlib import Path

from pprint import pprint
from loguru import logger

from simple_pp import simple_pp

CUR_DIR = Path(__file__).absolute().parent.as_posix()


def test_simple_pp_string_input():
    ''' test string input '''
    proxy = '127.0.0.1:8889'

    logger.debug(proxy)
    print('print: ', proxy)

    res = simple_pp(proxy)

    logger.debug(res)
    print('res: ', res)

    assert '127.0.0.1:8889' in str(res), 'autossh setup?'


def test_simple_pp_pkl1():
    ''' test pkl for simple_pp '''
    import sys
    import pickle
    from tqdm import tqdm

    from simple_pp.timeme import timeme

    logger.remove()
    logger.add(sys.stderr, level='INFO')

    repeat = 1

    pklfile = Path(CUR_DIR, 'res_info.pkl')
    logger.debug(f'pklfile: {pklfile}')
    res_info = pickle.load(open(pklfile, 'rb'))

    with timeme():
        res = simple_pp(res_info[:5])

    pprint([res, len(res)])

    assert len(res) == 5


def test_simple_pp_wrap():
    ''' test wrap '''
    proxy = ('200.89.178.208', True, True, 1.24)
    res = simple_pp(proxy)
    pprint(res)
    assert res


def test_simple_pp_no_wrap():
    ''' test wrap '''
    proxy = ('200.89.178.208', '127.0.0.1:8889')
    res = simple_pp(proxy)
    pprint(res)
    assert res


def test_simple_pp_freeip_top():
    from simple_pp.httpx_get import httpx_get
    from simple_pp.extract_ip_port import extract_ip_port

    resp = httpx_get('https://www.freeip.top/?page=1')
    res = simple_pp(extract_ip_port(resp.text))
    assert res
    assert len(res[0]) == 5


def test_localhost_8889():
    ''' localhost:8889 '''
    import sys

    res = simple_pp([['127.0.0.1:8889', 'user']])
    # [('127.0.0.1:8889', 'user', True, False, 0.83)]
    assert res[0][0] == '127.0.0.1:8889'
    if sys.platform in 'win32':  # local in win10
        assert res[0][-3] is True
        assert res[0][-2] is False


def test_localhost_8889__need_wrap():
    ''' localhost:8889 '''
    import sys

    res = simple_pp(['127.0.0.1:8889', 'user'])
    # [('127.0.0.1:8889', 'user', True, False, 0.83)]
    assert res[0][0] == '127.0.0.1:8889'

    # local in win10
    if sys.platform in ['win32']:
        assert res[0][-3] is True
        assert res[0][-2] is False
