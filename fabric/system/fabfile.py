# coding=utf-8

import sys, os
sys.path.append(os.path.join(os.getcwd(), "../.."))

from invoke import task, Collection, Config
from common import *

# from system import install, package, process
import system


@task
def config(c):
    print(Config())

ns = Collection(config, system)

