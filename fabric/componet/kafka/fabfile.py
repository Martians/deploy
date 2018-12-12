# coding=utf-8


import sys, os

from invoke import Collection

sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../../..")))
# print(sys.path)

from fabric import task
from common.hosts import *

from componet.flink import flink

@task
def config(c):
    print(Config())

ns = Collection(flink, config)

