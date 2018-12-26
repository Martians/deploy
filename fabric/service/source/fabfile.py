# coding=utf-8

import sys, os
sys.path.append(os.path.join(os.getcwd(), "../.."))

from invoke import task, Collection, Config

from common.init import *
from service import source

@task
def config(c):
    print(Config())

ns = Collection(config, source)

