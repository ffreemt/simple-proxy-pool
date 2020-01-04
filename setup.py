r'''
simple proxy pool + proxy validation
'''
# pylint: disable=invalid-name
from pathlib import Path
import re

from setuptools import setup, find_packages

name = """simple-proxy-pool"""
description = ' '.join(name.split('-')) + ' + proxy validation'
# dir_name, *_ = find_packages()
dir_name = 'simple_pp'
curr_dir = Path(__file__).parent


def read_requirements_file(*args):
    ''' paths, filename'''
    filepath = Path(*args)
    # logger.debug(f'\n\t {filepath} exists: {filepath.exists()}')
    if not filepath.exists():
        # logger.warning(f'{filepath} exists: {filepath.exists()}')
        print(f'{filepath} exists: {filepath.exists()}')
        return None
    try:
        lines = filepath.read_text('utf-8').split('\n')
    except Exception as exc:
        logger.error(exc)
        print(exc)
        return None

    # strip '#'
    lines = [elm.split('#', 1)[0].strip() for elm in lines]

    # remove empty lines
    return filter(None, lines)


# _ = open(f'{dir_name}/__init__.py').read()
_ = Path(f'{dir_name}/__init__.py').read_text(encoding='utf-8')
version, *_ = re.findall(r"__version__\W*=\W*'([^']+)'", _)
targz = 'v_' + version.replace('.', '') + '.tar.gz'

# install_requires = [*read_requirements_file(curr_dir, 'requirements.txt')]  # noqa

install_requires = ['requests',
 'aiohttp',
 'httpx',
 'multidict',
 'async_timeout',
 'html2text',
 'loguru',
 'tqdm',
 'pyperclip']

README_rst = f'{curr_dir}/README.md'
long_description = open(README_rst, encoding='utf-8').read() if Path(README_rst).exists() else ''

setup(
    name=name,
    packages=find_packages(),
    # packages=['simple_pp'],
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['machine translation', 'free', 'scraping', ],
    author="mikeee",
    url=f'http://github.com/ffreemt/{name}',
    download_url='https://github.com/ffreemt/yeekit-tr-free/archive/' + targz,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
    license='MIT License',
)
