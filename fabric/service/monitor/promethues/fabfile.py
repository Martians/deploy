# coding=utf-8

import sys, os
sys.path.append(os.path.join(os.getcwd(), "../.."))

from invoke import task, Collection, Config

from common import *
from service.monitor.promethues import prometheus

@task
def config(c):
    print(Config())


ns = Collection(prometheus)

