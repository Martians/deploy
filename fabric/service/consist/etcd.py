# coding=utf-8

import sys, os
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from invoke import task
from common import *
import system


class LocalConfig(LocalBase):
    def __init__(self):
        LocalBase.__init__(self, 'etcd')
        self.source = 'https://github.com/etcd-io/etcd/releases/download/v3.3.10/etcd-v3.3.10-linux-amd64.tar.gz'

        self.count = 3
        self.conf = '/etc/etcd.yml'
        self.path = '/var/lib/etcd'
        self.logs = '/var/log/etcd.log'

        self.peer_port = 2380
        self.client_port = 2379

        self.token = 'etcd-cluster'

        self.cluster = ''
        for host in hosts.lists(index=False, count=self.count):
            self.cluster = sep(self.cluster, '{name}=http://{host}:{port}'.format(name=host.name, host=host.host, port=self.peer_port))


local = LocalConfig()

@task
def install(c):
    """ install etcd

        https://github.com/etcd-io/etcd/blob/master/Documentation/op-guide/clustering.md
        https://blog.csdn.net/god_wot/article/details/77854093
    """
    c = hosts.one()
    download(c, local.name, source=local.source)
    copy_pack(c, dest=local.temp, async=True)

    for host in hosts.lists(index=False, count=local.count):
        c = hosts.conn(host)
        unpack(c, local.name, path=package(local.temp))

        c.run('''echo '
name: {name}
data-dir: {path}
listen-client-urls: http://{host}:{client_port},http://127.0.0.1:{client_port}
advertise-client-urls: http://{host}:{client_port},http://127.0.0.1:{client_port}

listen-peer-urls: http://{host}:{peer_port}
initial-advertise-peer-urls: http://{host}:{peer_port}

initial-cluster: {cluster}
initial-cluster-token: {token}
initial-cluster-state: new' > {conf}'''
              .format(name=host.name, path=host.item('disk', defv=local.path), host=host.host, client_port=local.client_port,
                      peer_port=local.peer_port, cluster=local.cluster, token=local.token, conf=local.conf), echo=False)
        c.run("cat {conf}".format(conf=local.conf))

@task
def clean(c):
    stop(c)

    for host in hosts.lists(index=False, count=local.count):
        c = hosts.conn(host)
        c.run("rm -rf {}".format(host.disk))

@task
def start(c):
    c = conn(c)

    for host in hosts.lists(index=False, count=local.count):
        c = hosts.conn(host)
        c.run('nohup /opt/etcd/etcd --config-file={conf} >> {log} 2>&1 &'
              .format(name=host.name, conf=local.conf, log=local.logs))

@task
def stop(c):
    c = conn(c)
    for host in hosts.lists(index=False, count=local.count):
        c = hosts.conn(host)
        c.run(system.kill('etcd', True), warn=True)

# install(hosts.one())
# start(hosts.conn(0))