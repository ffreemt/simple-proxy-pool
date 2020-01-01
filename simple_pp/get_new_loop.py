'''
get a usable new loop
'''

import asyncio

def get_new_loop():
    ''' get a new loop no matter what '''
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop
