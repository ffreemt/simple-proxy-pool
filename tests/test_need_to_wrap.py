'''
test need_to_wrap

    >>> assert not need_to_wrap(['127.0.0.1:8889', '127.0.0.1'])
    >>> assert need_to_wrap(['127.0.0.1:8889', 'source'])
'''

from simple_pp.need_to_wrap import need_to_wrap


def test_trivial():
    ''' trivial tests'''

    assert not need_to_wrap(['127.0.0.1:8889', '127.0.0.1'])

    # extract_ip_port (re.findall) converts to a list
    assert not need_to_wrap('127.0.0.1:8889')

    assert not need_to_wrap({})

    # need to convert to (['127.0.0.1:8889', 'source'],)
    # before feeding to simple_pp
    assert need_to_wrap(['127.0.0.1:8889', 'source'])
