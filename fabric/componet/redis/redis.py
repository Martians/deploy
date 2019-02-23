# coding=utf-8

from invoke import task
from common import *
import system


class LocalConfig(LocalBase):
    def __init__(self):
        LocalBase.__init__(self, 'redis')
        self.source = 'http://download.redis.io/releases/redis-5.0.0.tar.gz'
        self.temp = '/tmp'

        self.compile = '/tmp/compile'
        config_server()


local = LocalConfig()
name = 'redis'

""" 1. 准备 
        安装：fab install && fab cluster
        修改：fab clear && fab cluster （增加instance个数等）
        删除：fab clean
    
    2. 使用
        fab start stop stat
"""
@task
def install(c):
    install_prepare(c)
    install_master(c)
    install_slave(c)

@task
def cluster(c):
    stop(c)
    create_cluster(c)

    start(c)
    cluster_master(c)

    cluster_stat(c)

@task
def clear(c):
    c = hosts.conn(0)
    hosts.execute('cd {path}; rm nodes.conf server.log -rf'
                  .format(path=base(name), base=server.cluster.directory))

    for index in range(1, server.cluster.instance):
        hosts.execute('cd {path}/{base}/{index}; rm nodes.conf server.log -rf'
                      .format(path=base(name), base=server.cluster.directory, index=index))
    stop(c)

@task
def clean(c):
    stop(c)
    hosts.execute('rm {path} -rf'.format(path=base(name)))

@task
def start(c):
    hosts.execute("cd {path}; redis-server redis.conf".format(path=base(name)))

    for index in range(1, server.cluster.instance):
        hosts.execute('cd {path}/{base}/{index}; redis-server redis.conf'
                      .format(path=base(name), base=server.cluster.directory, index=index))
    stat(c)

@task
def stop(c):
    system.kills('redis-server')
    stat(c)

@task
def stat(c):
    hosts.execute("echo redis-server `ps aux | grep redis-server | grep -v 'grep' | wc -l`", out=True, hide=True)


########################################################################################################################
def install_prepare(c):
    """ 如果已经安装，就拒绝
    """
    command = disk._file_exist_command(base(name), dir=True)
    lists = hosts.conns_filter(command, conn=False)

    for host in lists:
        print("path [{}] already exist on host [{}]".format(base(name), host['host']))

    if len(lists):
        print("[{}] host not empty, source failed, please clean first!".format(len(lists)))
        exit(-1)

    """ 控制机下载安装包，复制到master
    """
    c = hosts.one()
    download(c, name, source=local.source)
    scp(c, hosts.get(0), package(), dest=local.temp)

    """ 安装包依赖
    """
    # system.source()


def install_master(c):
    c = hosts.conn(0)
    system.install(c, 'compile')
    unpack(c, name, path=package(local.temp), parent=local.compile)

    with c.cd(os.path.join(local.compile, 'redis')):
        if not file_exist(c, 'src', 'redis-server'):
            c.run("make MALLOC=libc -j5")

        c.run("mkdir -p {}".format(base(name)))
        with c.cd("src"):
            c.run("sudo \\cp redis-server redis-cli ../redis.conf {}".format(base(name)))
    configure(c)


def configure(c):
    sed.path(os.path.join(base(name), "redis.conf"))
    sed.grep(**{'prefix': '^'})

    sed.update(c, "bind", "0.0.0.0")
    sed.update(c, "daemonize", "yes")
    sed.update(c, "logfile", "server.log")
    sed.update(c, "stop-writes-on-bgsave-error", "no")

    sed.enable(c, "cluster-enabled", "yes")
    sed.enable(c, "cluster-config-file", "nodes.conf")

    sed.disable(c, "save", multi_line=True)


def install_slave(c):
    c = hosts.conn(0)
    copy_pack(c, base(name), other=True)

    """ 在每个机器，复制到 /usr/bin
    """
    hosts.execute("cd {base}; sudo \\cp redis-server redis-cli /usr/local/bin".format(base=base(name)))


########################################################################################################################
def cluster_stat(c):
    c = hosts.conn(0)
    c.run("echo CLUSTER NODES | redis-cli -c -p 6379".format())
    c.run("echo CLUSTER INFO | redis-cli -c -p 6379 | grep cluster_size".format())


def cluster_master(c):
    # exec.multi(c, '''
    #     yum source ruby rubygems -y
    #     curl -sSL https://rvm.io/mpapis.asc | gpg2 --import -
    #     curl -L get.rvm.io | bash -s stable
    #     find / -name rvm -print
    #     source /usr/local/rvm/scripts/rvm
    #     rvm list known
    #     rvm source 2.4.1
    #     rvm use 2.4.1
    #     rvm use 2.4.1 --default
    #     ruby --version''')
    #
    # exec.multi(c, '''
    #     wget https://rubygems.org/downloads/redis-4.0.3.gem
    #     gem source -l redis-4.0.3.gem ''')

    c = hosts.conn(0)
    lists = []
    for host in hosts.lists(index=False):
        lists.append("{}:{}".format(host['host'], 6379))

        for index in range(1, server.cluster.instance):
            lists.append("{}:{}".format(host['host'], (int(server.cluster.portbase) + index)))

    c.run("redis-cli --cluster create {} --cluster-replicas {}"
          .format(' '.join(lists), server.cluster.replica), pty=True, warn=True)


def create_cluster(c):
    temp = os.path.join(os.path.dirname(base(name)), "temp")
    hosts.execute('''
            mkdir -p {temp}; rm -rf {temp}/*
            mkdir -p {path}; rm -rf {path}/{base}
            '''.format(path=base(name), temp=temp,
                       base=server.cluster.directory))
    for index in range(1, server.cluster.instance):
        hosts.execute(''' 
          mkdir -p {temp}/{index}; cd {temp}/{index}
          cp {path}/redis.conf {temp}/{index}
          
          sudo sed -i "s#\(^port \).*#\\1{port}#g" redis.conf
          sudo sed -i "s#\(^pidfile [^0-9]*\)[0-9]*\([^0-9]\)#\\1{port}\\2#g" redis.conf
          '''.format(path=base(name), temp=temp,
                     base=server.cluster.directory, index=index,
                     port=(int(server.cluster.portbase) + index)))
    hosts.execute('''
            mv {temp} {path}/{base}
            '''.format(path=base(name), temp=temp,
                       base=server.cluster.directory))

@task
def help(c):
    c = conn(c, True)
    system.help(c, '''
    fab install && fab cluster
    fab stat
    
    fab clear && fab cluster
    fab clean
    ''')

if __name__ == '__main__':
    install(hosts.conn(0))
    # clean(hosts.conn(0))
    # cluster(hosts.conn(0))