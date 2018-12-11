# coding=utf-8


import sys, os

from invoke import Collection

sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
# print(sys.path)

from fabric import task
from common.hosts import *
from project.automatic import auto

@task
def config(c):
    print(Config())

ns = Collection(auto, config)

