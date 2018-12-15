# coding=utf-8
import os

from fabric import Connection, Config
import common.hosts as hosts

# import sys, os
# sys.path.append(os.path.dirname(os.getcwd()))
# sys.path.append(os.path.join(os.getcwd(), "../.."))
# sys.path.append(os.path.join(os.getcwd(), "../../.."))

# sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))


def copy_config():
    """ fabric 故障修复：确保当前目录下的yaml能够生效
        1. 比较 ./fabric.yaml 和 ~/.fabric.yaml 的差别
        2. 需要时，将./fabric.yaml 复制到 ~/.fabric.yaml
    """
    c = Connection("127.0.0.1")

    name = "fabric.yaml"
    origin = os.path.join(os.getcwd(), name)
    module = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)

    if os.path.exists(origin):
        src = origin
    elif os.path.exists(module):
        src = module
    elif os.path.exists("../" + name):
        src = "../" + name
    else:
        print("not find yaml!")
        exit(-1)

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


""" 默认配置内容
"""
default_config = {
    'install': {
        'parent': '/opt',
        'source': '/home/long/source'
    }
}


def init_config():
    pass


def base(name):
    if 'path' not in default_config['install']:
        c = Config()
        if 'install' in c and 'parent' in c.install:
            parent = c.install.parent
        else:
            parent = default_config['install']['parent']

        default_config['install']['path'] = os.path.join(parent, name)
    return default_config['install']['path']

if 1:
    copy_config()

    """ fabric config
    """
    fabric_config = Config()
    hosts.parse_info(fabric_config, fabric_config.user, fabric_config.connect_kwargs.password)

    init_config()


# 输出所有host信息
# hosts.dump()


if __name__ == '__main__':
    print(config.install.parent)