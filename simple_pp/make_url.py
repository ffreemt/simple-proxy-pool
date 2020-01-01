'''
preppend http:// if not present
'''

import re
import urllib  # pylint: disable=unused-import  # needed for typing
from urllib import parse

from loguru import logger


def make_url(
        url: str,
        schema: str = 'http',
) -> str:
    ''' prepent scheme (default http)
        http/https/socks if not present

    >>> make_url('http://127.0.0.1')
    'http://127.0.0.1'
    >>> make_url('htp://127.0.0.1')
    'http://127.0.0.1'
    >>> make_url('127.0.0.1')
    'http://127.0.0.1'
    >>> make_url('http://173.82.240.230:5000/json')
    'http://173.82.240.230:5000/json'
    '''

    if not isinstance(url, (bytes, str)):
        logger.warning(f'\n\t url provided: {url}, not str nor bytes, returning empty')
        return ''

    if isinstance(url, bytes):
        try:
            url = url.decode()
        except Exception as exc:
            logger.error(exc)
            logger.info(' Something is not right...')
            raise

    if parse.urlparse(url).scheme and not parse.urlparse(url).netloc:
    # if not parsed.netloc:  # notloc not present probably wrong format
        logger.warning(f'\n\t {url} probably malformed, trying to just extracting the ip')
        _ = re.search(r'\d+(\.\d+){3}', url)
        if _:
            url = _.group()

    if not parse.urlparse(url).scheme:
        try:
            _ = re.search(r'\d{1,4}(\.\d{1,4}){3}(:\d{1,4})?', url)
            if _:
                url = _.group()
        except Exception as exc:
            logger.error(f' {str(exc)} ')
            logger.info('Unable to retreve any valid ip, setting to 127.0.0.1')
            # url = '127.0.0.1'
            raise

    parsed = parse.urlparse(url)  # type: urllib.parse.ParseResult

    # proto not given, change to http,
    # if not parsed.scheme and parsed.path:

    if parsed.scheme not in ['http', 'https', 'ftp', 'socks4', 'socks5']:
        if parsed.netloc:
            netloc = parsed.netloc
        else:
            _ = re.search(r'\d{1,4}(\.\d{1,4}){3}(:\d{1,4})?', parsed.path)
            if _:  # attempt to retrieve an ip:port pair
                path_info = _.group()
            else:
                path_info = parsed.path

            netloc = path_info
        p_dict = {**parsed._asdict(), **{
            # 'scheme': 'http',
            'scheme': schema,
            'netloc': netloc,
            'path': '',
        }}  # type: dict

        parsed = parse.ParseResult(**p_dict)

        url = parse.urlunparse(parsed)

    return url
