'''
a tupl/list with the first entry as ip:port str

True if need to wrap in tuple

'''
from typing import Union
import re

def need_to_wrap(proxy: Union[str, tuple, list]) -> bool:
    '''
    True if proxy is a tupl/list with the first entry as ip:port str and other entries not ip:port

    >>> assert not need_to_wrap(['127.0.0.1:8889', '127.0.0.1'])
    >>> assert need_to_wrap(['127.0.0.1:8889', 'source'])
    '''
    if isinstance(proxy, str):
        return False

    if not isinstance(proxy, (list, tuple)):
        return False

    len_list = []
    for idx, elm in enumerate(proxy):
        try:
            _ = len(elm)
        except Exception as exc:
            _ = -idx
        finally:
            len_list.append(_)

    # all len equal
    all_eq = True
    all_eq = all(map(lambda x: len_list[0] == x, len_list[1:]))

    patt = re.compile(r'(?:https?://)?(\d{1,3}(?:\.\d{1,3}){3})(?:[\s\t:]+(\d{1,4}))?')
    if not all_eq:
        # check if all are ip:port
        ip_port_bool = []
        for elm in proxy:
            try:
                _ = patt.findall(elm)
            except Exception:
                _ = False
            finally:
                ip_port_bool.append(_)

        # a ip:port list/tuple already, no need to wrap
        if all(ip_port_bool):
            return False

        return True

    return False
