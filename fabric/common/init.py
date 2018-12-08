# coding=utf-8
import os

from fabric import Connection, Config
import common.hosts as hosts


def copy_config():
    """ fabric 故障修复：确保当前目录下的yaml能够生效
        1. 比较 ./fabric.yaml 和 ~/.fabric.yaml 的差别
        2. 需要时，将./fabric.yaml 复制到 ~/.fabric.yaml
    """
    c = Connection("127.0.0.1")

    name = "fabric.yaml"
    module = os.path.dirname(os.path.abspath(__file__)) + '/' + name

    if os.path.exists(module):
        src = module
    elif os.path.exists(name):
        src = name
    elif os.path.exists("../" + name):
        src = "../" + name

    dst = '~/.' + name

    if c.local("diff {} {}".format(src, dst), warn=True, echo=False).failed:
        c.local("\cp {} {}".format(src, dst))
        print("update config, try next time!")
        exit(-1)


def enable(c, f):
    """ 程序运行过程中，动态修改配置 run.warn

        全局配置为 run.warn = True；这里将 do work 中的操作，临时设置为 run.warn = False
        enable(c, 1)
        do work ...
        enable(c, 0)
    """
    c.config.run.warn = False if f else True

copy_config()

config = Config()
hosts.parse_info(config, config.user, config.connect_kwargs.password)

# 输出所有host信息
# hosts.dump()


