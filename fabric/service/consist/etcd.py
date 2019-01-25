# coding=utf-8

from invoke import task
from common import *
import system


class LocalConfig(LocalBase):
    def __init__(self):
        LocalBase.__init__(self, 'etcd')
        self.source = 'https://github.com/etcd-io/etcd/releases/download/v3.3.10/etcd-v3.3.10-linux-amd64.tar.gz'

        self.count = 1
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

""" https://github.com/etcd-io/etcd/blob/master/Documentation/docs.md

    https://github.com/etcd-io/etcd/blob/master/Documentation/op-guide/clustering.md
    https://blog.csdn.net/god_wot/article/details/77854093
        
"""
@task
def install(c):
    c = hosts.one()
    download(c, local.name, source=local.source)
    copy_pack(c, dest=local.temp)

    for host in hosts.lists(index=False, count=local.count):
        c = hosts.conn(host)

        unpack(c, local.name, path=package(local.temp))
        c.run('rm -rf {link}; ln -s {base}/etcdctl /usr/bin/'.format(base=local.base, link='/usr/bin/etcdctl'))

        sed.append(c, 'export ETCDCTL_API=3', file='/root/.bashrc')

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
def start(c, force=False):
    system.start('etcd', 'nohup /opt/etcd/etcd --config-file={conf} >> {log} 2>&1 &'
                  .format(conf=local.conf, log=local.logs), force=force, count=local.count)
@task
def stop(c):
    system.stop(local.name, count=local.count)

@task
def proc(c):
    system.proc(local.name, count=local.count)

@task
def clean(c):
    stop(c)
    system.clean(local.base, count=local.count)


""" etcdctl member list
    etcdctl cluster-health    
"""

# system.grep("etcd")
# install(hosts.one())
# start(hosts.conn(0))
# stop(hosts.conn(0))
# stat(hosts.conn(0))