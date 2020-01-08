r''' extrac ip port pairs from text
(\d{1,3}(?:\.\d{1,3}){3})(?:[^\d.]+(\d{1,5})(?=[^\d.]|$))?

flags=re.MULTILINE

(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:(?:\s+|\s*:)\d{1,5}(?![\d\.]))?

'''

from typing import List, Tuple, Union

import re
from pyquery import PyQuery as pq

from loguru import logger

PROXY_PAT = re.compile(r'(\d{1,3}(?:\.\d{1,3}){3})(?:[^\d.]+(\d{1,5})(?=[^\d.]|$))?')  # noqa
PROXY_PAT = re.compile(r'(\d{1,3}(?:\.\d{1,3}){3})(?:[^\d.]+(\d{1,5})(?=[^\d.]|$))?')  # noqa


def extract_ip_port(text: str, source: str = 'user') -> List[Tuple[str, str]]:
    ''' extract ip:port
    '''
    # from bs4 import BeautifulSoup
    from html2text import HTML2Text
    h2t = HTML2Text()
    h2t.ignore_links = True

    try:
        text = text.__str__()
    except Exception as exc:  # pragma: no cover
        logger.error(exc)
        raise

    logger.debug(f'\n\t {text[:30]} ')

    try:
        # _ = pq(text).text()
        # _ = BeautifulSoup(text, features='lxml').text
        text = h2t.handle(text)
    except Exception as exc:  # pragma: no cover
        logger.error(exc)
        text = ''

    proxies = []  # type: List[Union[str, Tuple[str, str]]]
    try:
        # _ = PROXY_PAT.findall(pq(Path(file).read_text('utf-8')).text())
        proxies = PROXY_PAT.findall(text)
    except Exception as exc:  # pragma: no cover
        logger.error(exc)
        proxies = []

    try:
        proxies = [elm[0] if len(elm) > 1 and not elm[1].strip() else ':'.join(elm) for elm in proxies]  # noqa
    except Exception as exc:  # pragma: no cover
        logger.error(exc)
        proxies = [str(exc)]

    return list(zip(proxies, [source] * len(proxies)))


def test_empty():  # pragma: no cover
    ''' test empty '''
    assert extract_ip_port('') == []


def test_127_0_0_1():  # pragma: no cover
    ''' test 127.0.0.1  '''
    assert extract_ip_port('127.0.0.1') == ['127.0.0.1']


def test_multilines():  # pragma: no cover
    ''' test empty '''
    assert extract_ip_port('127.0.0.1 \n\n 5000') == ['127.0.0.1:5000']  # noqa
