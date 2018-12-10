# coding=utf-8


import sys, os
sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
# print(sys.path)

""" 环境准备：    
    echo "/mnt/hgfs/local/deploy/fabric" > /home/long/.pyenv/versions/3.6.5/lib/python3.6/site-packages/test.pth
"""

from fabric import task
from project.automatic.auto import redis as redis

from common.hosts import *

@task
def install(c):
    redis.install(c)