'''
get proxies
'''

import inspect
from loguru import logger as log

from simple_pp.jhao.ProxyGetter.getFreeProxy import GetFreeProxy
from simple_pp.jhao.Util.utilFunction import verifyProxyFormat

member_list = inspect.getmembers(GetFreeProxy, predicate=inspect.isfunction)

# freeProxy01
# [*member_list[0][1]()]

proxy_count_dict = dict()
for func_name, func in member_list:
    log.info(u"开始运行 {}".format(func_name))
    try:
        proxy_list = [_ for _ in func() if verifyProxyFormat(_)]
        proxy_count_dict[func_name] = len(proxy_list)
    except Exception as e:
        log.info(u"代理获取函数 {} 运行出错!".format(func_name))
        log.error(str(e))

_ = '''
{'freeProxy01': 14,
 'freeProxy02': 0,
 'freeProxy03': 1000,
 'freeProxy04': 14,
 'freeProxy05': 30,
 'freeProxy07': 30,
 'freeProxy08': 46,
 'freeProxy09': 15,
 'freeProxy13': 0,
 'freeProxy14': 30}
# '''

# proxies = []
proxies_list = {}
for func_name, func in member_list:
    # proxies.extend([*member_list[0][1]()])
    # proxies.append()

    try:
        _ = [*func()]
    except Exception as exc:
        logger.error(f'\n\t {func_name}: {exc}')
        _ = []
    else:
        proxies_list.update({func_name: _})
