# -*- coding: utf-8 -*-
'''
args setup for simple_pp

'''
import sys

import argparse
from argparse import Namespace
import pyperclip

from loguru import logger


def get_args_simple_pp(lst=''):
    """
    args setup for simple_pp

    user input or files: fileinput
    proxies: stdin, files, pipe

    --service -s

    --anonymous -a (default: False)

    old
    -n --nosave -nosave (default=False), save file or not

    query metavar='query' [collect all if -i is False]
    parser.add_argument(nargs='*', metavar='query',
    dest='query', help='query terms (0 or more)', type=str),
    if empty, take from clipboard

    -o --output -output [stdout, browser, neither] (default=browser)

    """

    parser = argparse.ArgumentParser(
        description='simple proxy pool + proxy validation, brought to you by mu@qq41947782 2020.1.1'  # noqa
    )
    parser.add_argument(
        '-v',
        '-V',
        '--version',
        '-version',
        action='version',
        version='%(prog)s 0.0.1',
    )
    parser.add_argument(
        nargs='*',
        dest='proxies',
        metavar='free_format_proxy_or_files',
        type=str,
        help='free format proxies or filename(s) for file(s) containing free format proxies, if no input is given, the clipboard content will be used',  # noqa
    )
    parser.add_argument(
        '-p',
        '--proxies',
        dest='proxy_count',
        metavar='proxy_count',
        type=int,
        default=200,  # default None
        help='attempt to scrape this many proxies',
    )
    parser.add_argument(
        '-a',
        '--anonymous-only',
        dest='anonymous_only',
        action='store_true',
        help='show only anonymous proxies',
    )
    parser.add_argument(
        '-c',
        '--check',
        dest='check',
        action='store_true',
        help='check mode: just validate suppied proxies, do not fetch proxies from the net',
    )
    parser.add_argument(
        '-d',
        '--debug',
        dest='debug',
        action='store_true',
        help='turn debug on',
    )

    _ = '''
    parser.add_argument('-r', '--reorder', '-reorder', dest='reorder', action='append', choices=SITE_POOL, help='reorder part or complete of the website list')

    parser.add_argument('-e', '--exclude', '-exclude', dest='exclude', action='append', choices=SITE_POOL, help='exclude/remove some website(s)')

    parser.add_argument('-y', '--only', '-only', dest='only', action='append', choices=SITE_POOL, help='Only check selected website(s) ')  # modi --only

    #~ parser.add_argument('-s', '--save', '-save', dest='save', action='store_false', default=True, help='a file will be saved to the phrase_search  directory if set')

    parser.add_argument('-n', '--nosave', '-nosave', dest='nosave', action='store_true', default=False,
    help='Search result will not be saved to the phrases_searched  directory if set, probably ony useful with GoldenDict (with --output stdout)')

    parser.add_argument(nargs='*', dest='query', metavar='query', type=str, help='query terms (0 or more), if no input is given, the clipboard content (currently only the first line) will be used.')

    parser.add_argument('-o', '--output', '-output', dest='output', type=str, choices=['stdout', 'browser', 'neither'], default='browser', help='Set the output (default browser); stdout means the terminal, select stdout for GoldDict Programs plugin use')  # noqa

    parser.add_argument('-d', '--debug-level', dest='debug', type=int, choices=[10, 20, 30], default=20, help='Set the debug level (default 20 (info)); A larger value results in less verbose debug output')  # noqa
    parser.add_argument(
        '-v', '--version', '-version',
        action='version',
        version='%(prog)s 0.0.4',
    )
    # '''

    if isinstance(lst, str):
        lst = lst.split()

    if lst == []:
        args = parser.parse_args()
    else:
        args = parser.parse_args(lst)

    return args


def test_default():
    '''test default'''
    _ = get_args_simple_pp("")
    assert _ == Namespace(debug=False, proxies=[])


def test_proxies_input():
    '''test default'''
    _ = get_args_simple_pp('-d a b c \n x y z')
    assert _ == Namespace(
        debug=True, proxies=['a', 'b', 'c', 'x', 'y', 'z'])  # noqa


def test_debug_on_from_sys_argv():
    '''test default'''

    # save a copy of sys.argv
    sys_argv = sys.argv[:]

    sys.argv.append('-d')
    _ = get_args_simple_pp()
    assert _ == Namespace(debug=True, proxies=[])

    # restore sys.argv
    sys.argv = sys_argv[:]


def main():
    ''' main '''
    import fileinput

    from simple_pp.extract_ip_port import extract_ip_port

    # to test debug:
    # sys_argv = sys.argv[:]
    # sys.argv.append('-d')

    args = get_args_simple_pp()
    print(args)

    # unless args.debug is set (True), level set to 'INFO'
    # logger debug level is 'DEBUG', unless set to 'INFO'
    if args.debug:
        logger.remove()
        logger.add(sys.stderr, level='DEBUG')
    else:  # when debug is not set
        logger.remove()
        logger.add(sys.stderr, level='INFO')

    logger.debug(' debug msg ')
    logger.info(' info msg ')

    # sys.argv = sys_argv[:]

    logger.debug(args)

    proxies = ' '.join(args.proxies)

    # try pipe
    if not proxies:
        openhook = fileinput.hook_encoded(encoding='utf-8')
        text = ''.join(fileinput.input(openhook=openhook))  # type str

        logger.debug(f'text (from fileinput.input(): \n{text[:100]}')

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
        logger.info(
            f'\n{proxies[:20]}{"..." if len(proxies) > 20 else ""}, {len(proxies)}'
        )
    else:
        logger.warning('We tried hard, but were unable to obtain any proxies.')


if __name__ == "__main__":
    main()
