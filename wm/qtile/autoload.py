import time

config_file = "/home/irreq/github/config/wm/qtile/config.py"

def reload(module):
    """Reload a module
    Usage:
    reload(~/YOUR/PATH/TO/FILE.py) to access changes
    """
    with open(module) as f:
        code = compile(f.read(), module, 'exec')
        exec(code, globals(), locals())
count = 0
while count < 10:
    reload(config_file)
    count += 1
    time.sleep(1)
