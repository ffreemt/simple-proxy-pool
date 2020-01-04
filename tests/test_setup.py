'''
test path setup
'''
from pathlib import Path
import os
import sys
from setuptools import find_packages  # type: ignore

# import pytest
from loguru import logger

from simple_pp.jhao.ProxyGetter import getFreeProxy

# par_dir = Path(__file__).absolute().parent.parent
PAR_DIR = os.path.abspath(os.path.join(__file__, r'..\..'))
# sys.path.append(PAR_DIR)

logger.debug(f' PAR_DIR: {PAR_DIR}')

# from jhao.ProxyGetter import getFreeProxy  # type: ignore  # pylint: disable=wrong-import-position, import-error  # noqa

logger.debug(find_packages(PAR_DIR))
'''
# for path_ in find_packages('..'):
for path_ in find_packages(par_dir):
    sys.path.append((par_dir / Path(path_)).as_posix())
# '''

# logger.debug(sys.path)


def test_setup():
    '''
    test  path setup
    '''

    assert hasattr(getFreeProxy, 'GetFreeProxy')

    res = [*getFreeProxy.GetFreeProxy.freeProxy01()]
    print('print res: ', res)
    logger.debug(f'res: {res}')
    assert res
