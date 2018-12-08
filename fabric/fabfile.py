# coding=utf-8

import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

from fabric import task
import redis.redis as redis

from common.init import *
from common.hosts import *

@task
def install(c):
    redis.install(c)

@task
def cluster(c):
    redis.cluster(c)

@task
def clear(c):
    redis.clear(c)

@task
def start(c):
    redis.start(c)


@task
def stop(c):
    redis.stop(c)

@task
def stat(c):
    redis.stat(c)

@task
def clean(c):
    redis.clean(c)

@task
def config(c):
    print(Config())
