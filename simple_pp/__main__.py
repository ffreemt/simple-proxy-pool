''' __main__, to run:
python -m simple_pp

curl -s "https://www.freeip.top/?page=4" | python -m simple_pp

f = getattr(GetFreeProxy, SITE_LIST[0])
ip01 = [*zip(f(), [SITE_LIST[0]] * ilen(f()))]

'''
import pyperclip

from simple_pp import simple_pp  # , PROXYPOOL
# from proxybroker import Broker

from loguru import logger

from simple_pp.jhao.ProxyGetter.getFreeProxy import GetFreeProxy

SITE_LIST = ['freeProxy01', 'freeProxy04', 'freeProxy05', 'freeProxy07', 'freeProxy08', 'freeProxy09', 'freeProxy10', 'freeProxy11', 'freeProxy12', 'freeProxy14', 'freeProxy03']

# pragma: no cover
def main():
    '''main'''
    import sys
    from pathlib import Path
    import fileinput
    from pprint import pprint
    import fileinput

    from simple_pp.get_args_simple_pp import get_args_simple_pp
    from simple_pp.extract_ip_port import extract_ip_port

    args = get_args_simple_pp()

    if args.debug:
        logger.remove()
        logger.add(sys.stderr, level='DEBUG')
    else:  # when debug is not set
        logger.remove()
        logger.add(sys.stderr, level='INFO')

    logger.info(f'\n\t args: {args}')

    proxies = ' '.join(args.proxies)

    # try to load from files:
    files = []
    proxy_input = []
    for proxy in proxies:
        if Path(proxy).exists():
            files.append(proxy)
        else:
            proxy_input.append(proxy)

    # if not files:
    # try pipe if files empty
    if 1:
        openhook=fileinput.hook_encoded(encoding='utf-8')
        text = ''.join(fileinput.input(files, openhook=openhook))  # type str

        logger.debug(f'text (from fileinput.input(): \n{text[:100]}')

    if files:
        logger.info(f'{files} loaded')

    # append possible proxy input
    text += ' '.join(proxy_input)

    if text:
        logger.debug(f'\n\t text[:50]: \n{text[:50]}')
        proxies = extract_ip_port(text)

    if not proxies:
        proxies = pyperclip.paste()
        logger.info(" trying the clipboard")
        proxies = extract_ip_port(proxies)
    else:
        logger.info(" proxies from command line")

    if proxies:
        logger.info(f'\n{proxies[:20]}{"..." if len(proxies) > 20 else ""}, {len(proxies)}')
    else:
        logger.warning('We tried hard, but were unable to obtain any proxies.')
        return None

    logger.info(f'\n\t 验证中……\n')

    res = simple_pp(proxies)

    if res:
        print(f'\n\n 代理\t\t\t有效 \t匿名 \t响应时间')
        pprint([res, len(res)])
        print(f'\n\n 代理\t\t\t有效 \t匿名 \t响应时间')
    else:
        logger.info(' 并无任何可用代理…… ')

    _ = '''
    files = []
    for file in sys.argv[1:]:
        if Path(file).exists():
            files.append(file)

    if not files:
        pprint(' No file name provided or none exists.')
        pprint(' 未提供文件名或所提供文件名的文件不存在')
        print(f' 请将 ip 代理贴在下面，新起一行按 ctrl-Z加回车键 (Win)或 ctrl-D（Linux）结束 -- 同时按下Ctrl键和Z/D键）…………\n')
    else:
        print(f' 验证中……\n')

    text = ''
    for line in fileinput.input(files):
        text += line
    print(text[:50])

    pprint(' 按任意键退出。')
    _ = input()
    # '''

if __name__ == '__main__':
    main()
