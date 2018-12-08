# coding=utf-8
import os

from fabric import Connection, Config
import common.hosts as hosts

''' 确保当前目录下的yaml生效
        1. 比较 ./fabric.yaml 和 ~/.fabric.yaml 的差别
        2. ./fabric.yaml 复制到 ~/.fabric.yaml
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

    if c.local("diff {} {}".format(src, dst), warn=True, echo=False).failed:
        c.local("\cp {} {}".format(src, dst))
        print("update config, try next time!")
        exit(-1)


''' 如果希望动态修改默认配置
        假设全局配置为 run.warn = True；这里将包含的操作中，临时设置 run.warn = False
            enable(c, 1)
            do work ...
            enable(c, 0)
'''
def enable(c, f):
    c.config.run.warn = False if f else True


copy_config()

config = Config()
hosts.parse_info(config, config.user, config.connect_kwargs.password)

# 输出所有host信息
# hosts.list_host()


