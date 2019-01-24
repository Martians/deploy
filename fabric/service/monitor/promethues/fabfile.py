# coding=utf-8

from invoke import task, Collection, Config
from common import *
from service.monitor.promethues.prometheus import *

@task
def config(c):
    print(Config())


