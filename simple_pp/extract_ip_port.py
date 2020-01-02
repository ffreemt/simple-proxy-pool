r''' extrac ip port pairs from text
(\d{1,3}(?:\.\d{1,3}){3})(?:[^\d.]+(\d{1,5})(?=[^\d.]|$))?

flags=re.MULTILINE

(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:(?:\s+|\s*:)\d{1,5}(?![\d\.]))?

'''

from typing import List

import re
from pyquery import PyQuery as pq

from loguru import logger

PROXY_PAT = re.compile(r'(\d{1,3}(?:\.\d{1,3}){3})(?:[^\d.]+(\d{1,5})(?=[^\d.]|$))?')  # noqa
PROXY_PAT = re.compile(r'(\d{1,3}(?:\.\d{1,3}){3})(?:[^\d.]+(\d{1,5})(?=[^\d.]|$))?')  # noqa


def extract_ip_port(text: str) -> List[str]:
    ''' extract ip:port
    '''
    # from bs4 import BeautifulSoup
    from html2text import HTML2Text
    h2t = HTML2Text()
    h2t.ignore_links = True

    try:
        text = text.__str__()
    except Exception as exc:
        logger.error(exc)
        raise

    logger.debug(f'\n\t {text[:30]} ')

    try:
        # _ = pq(text).text()
        # _ = BeautifulSoup(text, features='lxml').text
        _ = h2t.handle(text)
    except Exception as exc:
        logger.error(exc)
        _ = ''

    try:
        # _ = PROXY_PAT.findall(pq(Path(file).read_text('utf-8')).text())
        _ = PROXY_PAT.findall(_)
    except Exception as exc:
        logger.error(exc)
        _ = []

    try:
        _ = [elm[0] if len(elm) > 1 and not elm[1].strip() else ':'.join(elm) for elm in _]  # noqa
    except Exception as exc:
        logger.error(exc)
        _ = [str(exc)]

    return _


def test_empty():
    ''' test empty '''
    assert extract_ip_port('') == []


def test_127_0_0_1():
    ''' test empty '''
    assert extract_ip_port('127.0.0.1') == ['127.0.0.1']


def test_multilines():
    ''' test empty '''
    assert extract_ip_port('127.0.0.1 \n\n 5000') == ['127.0.0.1:5000']  # noqa
