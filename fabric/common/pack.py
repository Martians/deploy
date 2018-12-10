# coding=utf-8
import os

from invoke import Responder
from common.disk import *
from common.init import *


def download(c, name, source=None, parent=None, local=None, temp="/tmp"):
    """ 下载并解压

        name：原生类型名字，最终将安装到 /opt/name
        path: 最终安装位置的父目录
        temp：临时文件路径，包括安装包等
        local：优先使用local作为数据源
        http：local不存在则到网上下载
    """
    parent = parent if parent else config['install']['path']
    local = local if local else config['install']['local']

    dest = '{}/{}'.format(parent, name)

    if file_exist(c, dest, dir=True):
        print("install path [{}] already exist".format(dest))
        return 1

    ###############################################################################################################
    ''' 传入了 source，就提取source中的版本号
            查找本地时，也使用该版本号
    '''
    package = os.path.basename(source) if source else name
    file_path = ''

    ###############################################################################################################
    """ 检查local是否存在
            1. local 直接是最终文件名
            2. local 是一个目录，搜索子目录
    """
    if file_exist(c, local):
        print("download, use [{}] in local config: {}".format(package, local))
        file_path = local
    else:
        # 如果source中包含了包名，此处搜索时就不需要再添加后缀；否则就用 tar.gz 或者 zip进行搜索
        file = file_search(c, local, package, suffix="tar.gz|zip" if package == name else None)
        if file:
            file_path = file
            print("download, get [{}] in local dir: {}".format(package, local))

    if file_path:
        c.run("\cp {} {} -rf".format(file_path, temp))

    else:
        """ 没有找到，需要下载
        """
        if not file_exist(c, temp, package):
            c.run("wget {} -P {}".format(source, temp))
        else:
            print("download, [{}] already download: {}".format(package, temp))
        file_path = '{}/{}'.format(temp, package)

    ###############################################################################################################
    ''' 解压到 path下，名称可能带有版本号 
    
        path下不能存在任何包含 name 的文件夹，否则无法判断哪个是解压出来后的目录
    '''
    c.run("mkdir -p {}".format(parent))
    if not file_actual(c, parent, name, dir=True):
        print("un-tar package [{}] ...".format(file_path))
        if file_path.endswith('tar.gz'):
            c.run("tar zxvf {} -C {} ".format(file_path, parent))
        elif file_path.endswith('zip'):
            c.run("unzip {} -d {} ".format(file_path, parent))
    else:
        print(1)

    ''' move，去掉名称中的版本号
    '''
    actual = file_actual(c, parent, name, dir=True)
    c.run("mv {}/{} {}/{}".format(parent, actual, parent, name))
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

    """ 1. 指定local具体位置
    """
    c.run("rm -rf /opt/redis; rm -rf /tmp/*redis*")
    download(c, "redis", source="http://download.redis.io/releases/redis-5.0.0.tar.gz",
             local="/home/long/source/component/redis/redis-5.0.0.tar.gz")

    """ 2. 指定local的目录，需要搜索
            但是默认local已经存在与 source 相同名字的包
    """
    c.run("rm -rf /opt/redis; rm -rf /tmp/*redis*")
    download(c, "redis", source="http://download.redis.io/releases/redis-5.0.0.tar.gz")

    ''' 3. 指定local的目录，需要搜索，并添加 tar.gz、zip后缀
            但是没有指定source，也不知道默认版本号
    '''
    c.run("rm -rf /opt/redis; rm -rf /tmp/*redis*")
    download(c, "redis")
