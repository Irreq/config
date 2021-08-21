"""This is the daemon file that will launch and manage events"""

import time

from . import vars


def reload(module):
    """Reload a module
    Usage:
    reload(~/YOUR/PATH/TO/FILE.py) to access changes
    """
    with open(module) as f:
        code = compile(f.read(), module, 'exec')
        exec(code, globals(), locals())

def test():
    print(f"{__file__} loaded @ {time.time()}")

# if __name__ == "__main__":
#     test()
