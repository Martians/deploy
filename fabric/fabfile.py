# coding=utf-8

import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

from fabric import task
from common.common import *
from common.hosts import *
from redis.redis import *

@task
def install(c):
    install_varify(conn(0))
    install_master(conn(0))
    install_slave(conn(0))

@task
def clear(c):
    redis_clear(c)


@task
def start(c):
    redis_start(c)


@task
def stop(c):
    redis_stop(c)

@task
def config(c):
    print(Config())

@task
def stat(c):
    redis_stat(c)
