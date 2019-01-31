# coding=utf-8

from invoke import task
from common import *
import system


class LocalConfig(LocalBase):
    """ 默认配置
    """
    def __init__(self):
        LocalBase.__init__(self, 'grafana')

        self.source = 'https://dl.grafana.com/oss/release/grafana-5.4.3.linux-amd64.tar.gz'


""" 提供个默认参数
    
    该变量定义在头部，这样在函数的默认参数中，也可以使用了
"""
local = LocalConfig()

@task
def install(c):
    c = hosts.one()
    download(c, local.name, source=local.source)

    scp(c, hosts.get(0), package(), dest=local.temp)
    unpack(conn(0), local.name, path=package(local.temp))

    """ 手动安装：
        plugin: data/plugins
                使用 grafana-cli plugins install grafana-piechart-panel，安装的位置在 /var/lib/grafana/plugins
    """


def configure(c):
    c.run('sudo grafana-cli plugins install grafana-piechart-panel')

@task
def help(c):
    c = conn(c, True)
    system.help(c, '''
    only support install now''')

# install(hosts.conn(0))