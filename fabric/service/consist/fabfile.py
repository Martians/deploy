# coding=utf-8

import sys, os
sys.path.append(os.path.join(os.getcwd(), "../.."))

from invoke import task, Collection, Config

from common import *
from service.consist import *

@task
def config(c):
    print(Config())

ns = Collection(config)
ns.add_collection(etcd)




