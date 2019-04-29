# coding=utf-8

from invoke import task, Collection, Config

from common import *
from componet.kafka import kafka

@task
def config(c):
    print(Config())

ns = Collection(kafka)

