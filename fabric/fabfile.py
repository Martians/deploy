# coding=utf-8

import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

from fabric import task
from redis.common import *
from redis.redis import *


@task
def install(c):
    install_master(hosts[0])

@task
def clear(c, name):
    pass


@task
def start(c, name):
    pass


@task
def stop(c, name):
    pass

@task
def config(c):
    print(Config())