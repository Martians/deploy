# coding=utf-8
import os

from invoke import Responder
from common.disk import *
from common.init import *

def download(c, name, http, local=None, path=None, temp="/tmp"):
    """ 下载并解压

        name：原生类型名字，最终将安装到 /opt/pack_name
        path: 最终安装位置的父目录
        temp：临时文件路径，包括安装包等
        local：优先使用local作为数据源
        http：local不存在则到网上下载
    """
    path = path if path else '/opt'
    dest = '{}/{}'.format(path, name)
    if file_exist(c, dest, dir=True):
        print("install path [{}] already exist".format(dest))
        return 1

    ''' 1. local 是否存在
        2. 是否已经download过了
        3. 执行download
    '''
    if local and file_exist(c, local):
        srcs = local
    else:
        package = os.path.basename(http)
        if not file_exist(c, temp, package):
            c.run("wget {} -P {}".format(http, temp))
        srcs = '{}/{}'.format(temp, package)

    ''' 解压到 path下，名称可能带有版本号 
    
        path下不能存在任何包含 name 的文件夹，否则无法判断哪个是解压出来后的目录
    '''
    c.run("mkdir -p {}".format(path))
    if not file_actual(c, path, name, dir=True):
        print("un-tar package [{}] ...".format(srcs))
        c.run("tar zxvf {} -C {} ".format(srcs, path))

    ''' move，去掉名称中的版本号
    '''
    actual = file_actual(c, path, name, dir=True)
    c.run("mv {}/{} {}/{}".format(path, actual, path, name))
    return 0


def copy_slave(c, path, sshpass=False):
    """ scp
        1. 使用sshpass，主机需要先安装
            sshpass -p 111111 scp -r /opt/redis/ root@192.168.0.81:/tmp

        2. 使用Responder
    """
    for host in hosts.lists(index=False, other=True):
        user = hosts.get_host_item(host, "user")
        paww = hosts.get_host_item(host, "pass")
        command = "scp -r {} {}@{}:{}".format(path, user, host['host'], os.path.dirname(path))

        if sshpass:
            c.run("sshpass -p {} {}".format(paww, command))
        else:
            sudopass = Responder(pattern=r'.*password:', response=paww + '\n')
            c.run(command, pty=True, watchers=[sudopass])


if __name__ == '__main__':
    from fabric import Config, Connection

    c = hosts.conn(0)

    c.run("rm -rf /opt/redis")
    download(c, "redis", http="http://download.redis.io/releases/redis-5.0.0.tar.gz",
             local="/home/long/source/component/redis/redis-5.0.0.tar.gz")

    c.run("rm -rf /opt/redis")
    download(c, "redis", http="http://download.redis.io/releases/redis-5.0.0.tar.gz")