from . import daemon, vars, status
print(2)
if vars.test:
    daemon.test()
    status.test()
