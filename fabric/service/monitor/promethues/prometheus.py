# coding=utf-8

# import sys, os
# sys.path.append(os.path.join(os.getcwd(), "../.."))

from invoke import task
from common import *
import system


class LocalConfig(LocalBase):
    """ 默认配置
    """
    def __init__(self):
        LocalBase.__init__(self, 'prometheus')

        self.source = 'https://github.com/prometheus/prometheus/releases/download/v2.6.0/prometheus-2.6.0.linux-amd64.tar.gz'
        self.config = 'prometheus.yml'

        self.node_source = 'https://github.com/prometheus/node_exporter/releases/download/v0.17.0/node_exporter-0.17.0.linux-amd64.tar.gz'
        self.node_name = 'node_exporter'
        self.node_port = 9100

        self.node_config = 'node.yaml'
        self.client_config = 'client.yaml'

        self.alert = 'https://github.com/prometheus/alertmanager/releases/download/v0.16.0-beta.0/alertmanager-0.16.0-beta.0.linux-amd64.tar.gz'


""" 提供个默认参数
    
    该变量定义在头部，这样在函数的默认参数中，也可以使用了
"""
local = LocalConfig()

@task
def install_server(c):
    c = hosts.one()
    download(c, local.name, source=local.source)

    """ 安装包下载后，到master上进行解压
    """
    scp(c, hosts.get(0), package(), dest=local.temp)
    unpack(conn(0), local.name, path=package(local.temp))

    config_server(conn(0))


def config_server(c):
    sed.path(os.path.join(local.base, local.config))

    """ 配置文件
    """
    file_sd_node = """ 
  - job_name: 'node'
    file_sd_configs:
    - files:
      - '{node}'""".format(node=local.node_config)

    file_sd_client = """ 
  - job_name: 'client'
    scrape_interval: 1s
    file_sd_configs:
    - files:
      - '{client}'""".format(client=local.client_config)

    sed.append(c, file_sd_node)
    sed.append(c, file_sd_client)

    """ file service discovery
    """
    with c.cd(local.base):
        c.run("""echo '
- labels:
    type: 'node'
        
  targets:' > {node}""".format(node=local.node_config))

        c.run("""echo '
- labels:
    type: 'client'

  targets:' > {client}""".format(client=local.client_config))


@task
def install_node(c):
    c = hosts.one()

    download(c, local.node_name, source=local.node_source)
    copy_pack(c, dest=local.temp)

    hosts.execute('sudo rm -rf /opt/*{}*'.format(local.node_name))

    for index in hosts.lists():
        unpack(hosts.conn(index), local.node_name, path=package(local.temp))

    config_server_node(c)


def config_server_node(c):
    c = hosts.conn(0)

    append = ''
    for host in hosts.lists(index=False):
        append += "    - '{}:{}'\n".format(host.host, local.node_port)

    sed.path(os.path.join(local.base, local.node_config))
    sed.append(c, append)

@task
def start_server(c):
    c = hosts.conn(0)
    c.run(system.nohup('cd {}; nohup ./prometheus --config.file={}'.format(local.base, local.config)), pty=True)

@task
def stop_server(c):
    c = hosts.conn(0)
    c.run('{}'.format(system.kill('prometheus', string=True)))

@task
def start_node(c):
    system.start(local.node_name, system.nohup('cd {}; nohup ./node_exporter --web.listen-address=":{}"'
                                               .format(base(local.node_name), local.node_port)), pty=True)

@task
def stop_node(c):
    system.stop(local.node_name)

@task
def clean(c):
    stop_server(c)
    stop_node(c)

    system.clean('/opt/{}, /opt/{}'.format(local.name, local.node_name))


@task
def install_alert(c):
    pass
    # hosts.execute('sudo rm -rf /opt/*kafka*')
    #
    # for index in hosts.lists():
    #     unpack(hosts.conn(index), local.name, path=package(local.temp))


# install_server(conn(0))
# install_node(conn(0))
# start_server(conn(0))
# stop(conn(0))
# clean(conn(0))
# start_node(conn(0))