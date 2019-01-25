
from invoke import task, Collection, Config

from common import init

@task
def config(c):
    print('hosts config ----- [{}]\n'.format(init.search_config('hosts.yaml')))
    print('fabric config: ')
    print(Config())