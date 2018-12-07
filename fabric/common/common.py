# coding=utf-8
import os

from fabric import Connection, Config
import common.hosts as hosts

''' 将当前工程目录下的 fabric.yaml 复制出去
'''
def copy_config():
    c = Connection("127.0.0.1")

    module = os.path.dirname(os.path.abspath(__file__)) + "/fabric.yaml"

    if os.path.exists(module):
        src = module
    elif os.path.exists("fabric.yaml"):
        src = "fabric.yaml"
    elif os.path.exists("../fabric.yaml"):
        src = "../fabric.yaml"

    dst = "~/.fabric.yaml"

    if c.local("diff {} {}".format(src, dst), warn=True).failed:
        c.local("\cp {} {}".format(src, dst))
        print("update config, try next time!")
        exit(-1)


def enable(c, f):
    c.config.run.warn = False if f else True


copy_config()

config = Config()
hosts.parse_info(config, config.user, config.connect_kwargs.password)

# 输出所有host信息
# hosts.list_host()


