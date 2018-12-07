# coding=utf-8
import os

from fabric import Connection, Config
import redis.hosts as hosts

''' 将当前工程目录下的 fabric.yaml 复制出去
'''
def copy_config():
    c = Connection("127.0.0.1")
    src = os.path.dirname(os.path.abspath(__file__)) + "/fabric.yaml"
    dst = "~/.fabric.yaml"

    if c.local("diff {} {}".format(src, dst), warn=True).failed:
        c.local("\cp {} {}".format(src, dst))
        print("update config, try next time!")
        exit(-1)

copy_config()

hosts.parse_info(Config())
hosts.list_host()