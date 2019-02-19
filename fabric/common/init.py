# coding=utf-8
import os

from fabric import Connection, Config
from common.host import hosts
from common.util import *

""" 搜索路径：
    1. 方案1：加入到系统搜索路径，执行 python prepare.py即可
    
    2. 方案2：启动时加入，在执行py的头部加入以下类似语句，根据实际路径选择
        import sys, os
        sys.path.append(os.path.join(os.getcwd(), "../.."))
        
        sys.path.append(os.path.dirname(os.getcwd()))
        sys.path.append(os.path.join(os.getcwd(), "../../.."))
        sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))        
"""


def search_config(name):
    """ 当前目录 yaml
    """
    origin = os.path.join(os.getcwd(), name)

    """ 全局目录
    """
    user_home = '{}/{}'.format(os.path.expanduser('~'), name)
    glob_etc = '/etc/{}'.format(name)

    """ 顶层目录 yaml
    """
    module = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    module = os.path.join(os.path.abspath(module), name)

    if os.path.exists(origin):
        src, pos = origin, 'pwd'

    elif os.path.exists(user_home):
        src, pos = user_home, 'user home'
    elif os.path.exists(glob_etc):
        src, pos = glob_etc, '/etc'

    elif os.path.exists(module):
        src, pos = module, 'module'
    else:
        print('not find {}!'.format(name))
        exit(-1)

    return src


def hosts_config():
    name = global_define.config.hosts
    return search_config(name)


def config_server(withdraw=True):
    """ 将本地所有的 yaml 配置文件，聚合起来
    """
    collect = []

    def traverse(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.find('yaml') != -1 or file.find('yml') != -1:
                    collect.append(os.path.join(root, file))

            for dir in dirs:
                if not dir.startswith('_'):
                    traverse(os.path.join(root, dir))
            break
    traverse('.')

    for file in collect:
        with open(file, 'r') as f:
            import yaml
            conf = Dict(yaml.load(f))
            server.update(conf)

    if withdraw:
        server.withdraw()
    return collect


def config_fabric():
    """ fabric 配置文件：当前目录、用户目录、全局目录、工程目录（默认配置）
        1. 比较找到的 fabric.yaml 和 ~/.fabric.yaml 的差别
        2. 需要时，将 fabric.yaml 复制到 ~/.fabric.yaml
    """
    c = Connection("127.0.0.1")

    name = 'fabric.yaml'
    src = search_config(name)

    dst = '~/.' + name
    if c.local("diff {} {}".format(src, dst), warn=True, echo=False).failed:
        c.local("\cp {} {}".format(src, dst))
        print("update config, try next time!")
        exit(-1)


def config_hosts():
    fabric_config = Config()

    user, paww = fabric_config.user, fabric_config.connect_kwargs.password
    hosts.parse(hosts_config(), user=user, paww=paww)

""" 默认配置内容
"""
global_define = Dict({
    'config': {
        'hosts': 'hosts.yaml'
    },
    'source': {
        'parent': '/opt',
        'source': '/home/long/source'
    }
})


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
        parent = global_define['source']['parent']
    return os.path.join(parent, name)

    # global_define['source']['path'] = os.path.join(parent, name)
    # return global_define['source']['path']


def conn(c, one=False):
    """ 确保传入的是connect，不是local的context
    """
    if not hasattr(c, 'host'):
        c = hosts.one() if one else hosts.conn(0)
        print("connection [{}]".format(c.host))
    return c


def lc(c):
    return Connection("127.0.0.1")


def parse_argv():
    import sys
    print(sys.argv[1:])


if 1:
    config_fabric()

    config_hosts()

    server = Dict()

