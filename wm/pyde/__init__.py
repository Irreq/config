from . import daemon, vars, status

if vars.test:
    daemon.test()
    status.test()
