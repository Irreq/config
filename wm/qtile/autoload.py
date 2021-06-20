config_file = "/home/irreq/github/config/wm/qtile/config.py"
with open(config_file) as f:
    code = compile(f.read(), config_file, 'exec')
    exec(code, globals(), locals())
