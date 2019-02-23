# coding=utf-8
import os

from fabric import Connection, Config
from common.host import hosts
from common.util import *
from common.disk import *
from common.config import *

""" 搜索路径：
    1. 方案1：加入到系统搜索路径，执行 python prepare.py即可
    
    2. 方案2：启动时加入，在执行py的头部加入以下类似语句，根据实际路径选择
        import sys, os
        sys.path.append(os.path.join(os.getcwd(), "../.."))
        
        sys.path.append(os.path.dirname(os.getcwd()))
        sys.path.append(os.path.join(os.getcwd(), "../../.."))
        sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))        
"""


def config_fabric():
    """ fabric 配置文件：当前目录、用户目录、全局目录、工程目录（默认配置）
        只有配置在 ~/.fabric.yaml 和 /etc/fabric.yaml 的才能真正生效（此处选择~/.fabric.yaml）

        1. 比较找到的 fabric.yaml 和 ~/.fabric.yaml 的差别
        2. 需要时，将 fabric.yaml 复制到 ~/.fabric.yaml
    """
    c = Connection("127.0.0.1")

    name = 'fabric.yaml'
    src = search_config(name)

    dst = '~/.' + name
    if not file_exist(c, dst):
        print('copy config, try next time!')
        restart = True

    elif c.local("diff {} {}".format(src, dst), warn=True, echo=False).failed:
        print("update config, try next time!")
        restart = True

    if restart:
        c.local("\cp {} {}".format(src, dst))
        exit(-1)


def config_hosts():
    fabric_config = Config()
    user, paww = fabric_config.user, fabric_config.connect_kwargs.password

    path = search_config(globing.config.hosts)
    hosts.parse(path, user=user, paww=paww)


def config_server(withdraw=True):
    """ 将本地所有的 yaml 配置文件，聚合起来
    """
    config = parse_traverse('.', withdraw=withdraw)
    server.update(config)


class LocalBase:
    def __init__(self, name=''):
        self.temp = '/tmp'
        self.name = name
        self.base = base(self.name)


def base(name):
    """ 程序安装路径
    """
    # if 'path' not in global_define['source']:

    c = Config()
    """ 如果配置文件中已经设置了路径，就使用
    """
    if 'source' in c and 'parent' in c.install:
        parent = c.install.parent
    else:
        parent = globing['source']['parent']
    return os.path.join(parent, name)

    # global_define['source']['path'] = os.path.join(parent, name)
    # return global_define['source']['path']


def conn(c, one=False):
    if globing.invoke:
        from invoke import Context
        c = Context(Config())
        c.host = 'local'
        return c

    """ 确保传入的是connect，不是local的context
    """
    if not hasattr(c, 'host'):
        c = hosts.one() if one else hosts.conn(0)
        print("connection [{}]".format(c.host))
    return c


def set_invoke(set):
    hosts.invoke = set
    globing.invoke = set


def parse_argv():
    import sys
    print(sys.argv[1:])


if 1:
    config_fabric()

    config_hosts()

    server = Dict()

