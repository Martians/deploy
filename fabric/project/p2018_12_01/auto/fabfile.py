# coding=utf-8

import sys, os
sys.path.append(os.path.join(os.getcwd(), "../.."))

from invoke import task, Collection, Config

from common import *
from project.p2018_12_01.auto import auto

@task
def config(c):
    print(Config())

ns = Collection(auto)

