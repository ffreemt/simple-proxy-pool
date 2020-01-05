''' __main__, to run:
python -m simple_pp

curl -s "https://www.freeip.top/?page=4" | python -m simple_pp

f = getattr(GetFreeProxy, SITE_LIST[0])
ip01 = [*zip(f(), [SITE_LIST[0]] * ilen(f()))]

'''
from typing import List

import pyperclip
from loguru import logger

from simple_pp import simple_pp  # , PROXYPOOL
from simple_pp.get_proxies import get_proxies
# from proxybroker import Broker

# from simple_pp.jhao.ProxyGetter.getFreeProxy import GetFreeProxy

SITE_LIST = [
    'freeProxy01', 'freeProxy04', 'freeProxy05', 'freeProxy07', 'freeProxy08',
    'freeProxy09', 'freeProxy10', 'freeProxy11', 'freeProxy12', 'freeProxy14',
    'freeProxy03'
]


# pragma: no cover
def main():  # pylint: disable=too-many-branches, too-many-locals, too-many-statements  # noqa
    '''main'''
    import sys
    from pathlib import Path
    import fileinput
    from pprint import pprint

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

    # proxies = ' '.join(args.proxies)

    # try to collect file names and other stdin input proxies:
    files = []
    proxy_input = []
    for proxy in args.proxies:
        try:
            _ = Path(proxy).exists() and Path(proxy).is_file()
        except Exception as exc:
            _ = False
        if _:
            files.append(proxy)
        else:
            proxy_input.append(proxy)

    logger.info(f' files: {files}')

    text = ''
    if files:
        openhook = fileinput.hook_encoded(encoding='utf-8')
        text = ''.join(fileinput.input(files, openhook=openhook))  # type str

        logger.debug(f'text (from fileinput.input(): \n{text[:100]}')
        logger.info(f'{files} loaded')

    # try pipe if files empty

    # append possible stdin proxy input
    text += ' '.join(proxy_input)

    proxies = []  # List[Any]
    if text:
        logger.debug(f'\n\t text[:50]: \n{text[:50]}')
        proxies = extract_ip_port(text)

    # Try clipboard
    if not proxies:
        logger.info(" trying the clipboard")
        try:
            proxies = extract_ip_port(pyperclip.paste())
        except Exception as exc:
            logger.warning(exc)
    else:
        logger.info(" proxies from command line")
    """
    # Try stdin
    if not proxies:
        # pprint(' No file name provided or none exists.')
        pprint(' 未提供文件名或代理地址或所提供文件名的文件不存在')
        print(
            f' 请将 ip 代理贴在下面，可多行，格式不限，新起一行按 ctrl-Z加回车键 (Win)或 ctrl-D（Linux）结束 (ctrl-Z既是同时按下Ctrl键和Z键)…………\n'
        )

        _ = '''
        text = ''
        for line in fileinput.input(files):
            text += line
        # '''

        text = ''.join(fileinput.input(files))

        logger.debug(f'stdin: {text[:50]}')
        proxies = extract_ip_port(text)
        logger.debug(f'stdin: {proxies}')

    if proxies:
        logger.info(
            f'\n{proxies[:20]}{"..." if len(proxies) > 20 else ""}, {len(proxies)}'
        )
    else:
        # logger.warning('We tried hard, but were unable to obtain any proxies.')
        logger.info('\n\t很努力试过很多方法无法获取代理地址。')
    # """

    try:
        tot_no = len(proxies)
    except Exception as exc:
        logger.error(exc)
        tot_no = 0

    # obtain additional proxies if -c is not set (False)
    if tot_no < args.proxy_count and args.check is False:

        logger.info(' 试着从网上获取代理地址…… ')
        if not args.debug:
            logger.info(' 可使用 -d 显示详情, 例如： \n\t python -m simple_pp -d')
        if args.proxy_count - tot_no > 5000:
            logger.info(' 可能需要一些时间……')

        temp = get_proxies(args.proxy_count - tot_no)
        logger.info(f' 成功获取 {len(temp)}个代理地址……')
        logger.debug(temp)

        proxies.extend(temp)

    logger.debug(proxies)
    logger.debug(len(proxies))

    logger.info(f'\n\t 验证中……\n')

    res = simple_pp(proxies)
    logger.debug(res)

    filter_flag = -3
    if args.anonymous_only:
        filter_flag = -2

    res = sorted(
        [elm for elm in res if elm[filter_flag] is True],
        key=lambda x: x[-1],
        reverse=True)

    # try to get from the pool
    # for elm in SITE_LIST[:-1]:

    # xici: 3985  pages anonymous, 738 normal proxies

    _ = '''
    # checking p and a options:
    # none not set
    if args.tot_anonymous is None and args.tot_proxies is None:
        args.tot_proxies = 20
    # both set, resest tot_anonymous
    if args.tot_anonymous and args.tot_proxies:
        args.tot_anonymous = None
    logger.debug(f'tot_proxies/tot_anonymous: {}/{}')

    # set filter, tot_proxies-> -3, tot_anonymous-> -2
    if args.tot_proxies:
        filter_flag = -2
        target_no = args.tot_proxies
    if args.tot_anonymous:
        filter_flag = -3
        target_no = args.tot_anonymous
    # '''

    if res:
        print(f'\n\n 代理\t\t\t源 \t有效 \t匿名 \t响应时间')
        pprint(res)
        pprint(['total:', len(res)])
        if len(res) > 20:
            print(f'\n\n 代理\t\t\t源 \t有效 \t匿名 \t响应时间')
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
