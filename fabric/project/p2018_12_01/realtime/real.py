# coding=utf-8
import os

from fabric import Connection, SerialGroup as Group, Config, task

from common import *
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