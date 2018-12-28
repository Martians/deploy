# coding=utf-8

import sys, os
sys.path.append(os.path.join(os.getcwd(), "../.."))

from invoke import task, Collection, Config

from common import *
from componet.redis import redis

@task
def config(c):
    print(Config())


ns = Collection(redis)
