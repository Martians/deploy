# coding=utf-8
import os

from fabric import Connection, SerialGroup as Group, Config, task

from common.init import *
from common.pack import *

import common.hosts as hosts
import common.sed as sed
from componet.flink import flink

@task
def install(c):
    flink.install(c)

@task
def coding(c):
    pass

@task
def compile(c):
    pass

@task
def update(c):
    pass

@task
def clean(c):
    pass