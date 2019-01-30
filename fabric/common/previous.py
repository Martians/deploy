
from invoke import task, Collection, Config

from common.init import *

@task
def config(c, fabric=False):
    name = global_define.config.hosts
    print('hosts config  ----- [{}]'.format(search_config(name)))

    name = config_server()
    if len(name):
        print('server config ----- [{}]\n'.format(name[0]))
    else:
        print('')

    if fabric:
        print('fabric config: ')
        print(Config())

@task
def kill(c, name):
    import system
    system.process.kills(name)

