# coding=utf-8
import os

from fabric import Connection, SerialGroup as Group, Config

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

config = Config()

hosts = Group(*config.hosts)
copy_config()