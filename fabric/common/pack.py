# coding=utf-8
import os

from invoke import Responder
from common.disk import *
from common.init import *


def download(c, name, source=None, local=None, path="/tmp"):
    """ 下载并解压
        name：原生类型名字，用于查找安装包
        path：安装包下载路径

        local： 优先使用local作为数据源
        source：local不存在则到网上下载
    """
    local = local if local else default_config['install']['source']

    ''' 传入了source，就提取source中的版本号
            查找本地时，也使用该版本号
    '''
    package = os.path.basename(source) if source else name
    file_path = ''

    ###############################################################################################################
    """ 1. 检查local是否存在
            1. local 直接是最终文件名
            2. local 是一个目录，搜索子目录
    """
    if file_exist(c, local):
        print("download, use local config: [{}]".format(local))
        file_path = local
    else:
        # 如果source中包含了包名，此处搜索时就不需要再添加后缀；否则就用 tar.gz 或者 zip进行搜索
        file = file_search(c, local, package, suffix="tar.gz|zip" if package == name else None)
        if file:
            file_path = file
            print("download, already in local: [{}]".format(file_path))

    """ 2. 没有找到，需要下载
    """
    if not file_path:
        file_path = '{}/{}'.format(path, package)

        if file_exist(c, path, package):
            print("download, already download: [{}]".format(file_path))
        else:
            c.run("wget {} -P {}".format(source, path))
            print("download, http download [{}]".format(file_path))
    default_config['install']['package'] = file_path


def package():
    return default_config['install']['package']


def unpack(c, name, path, parent=None):
    dest = '{}/{}'.format(parent, name)

    if file_exist(c, dest, dir=True):
        print("install path [{}] already exist".format(dest))
        return 1

    """ 解压到 path下，名称可能带有版本号

        path下不能存在任何包含 name 的文件夹，否则无法判断哪个是解压出来后的目录
    """
    parent = parent if parent else default_config['install']['parent']

    c.run("mkdir -p {}".format(parent))
    if not file_actual(c, parent, name, dir=True):
        print("un-tar package [{}] ...".format(path))

        if path.endswith('zip'):
            c.run("sudo unzip {} -d {} ".format(path, parent))
        else:
            c.run("sudo tar zxvf {} -C {} ".format(path, parent))
    else:
        print(1)

    ''' move，去掉名称中的版本号
    '''
    actual = file_actual(c, parent, name, dir=True)
    c.run("sudo mv {}/{} {}/{}".format(parent, actual, parent, name))


def copy_pack(c, path, dest=None, sshpass=False, other=False, async=False):

    if async:
        """ 异步线程方式执行，需要已经设置了免密码登陆
        """
        host = hosts.one(True)
        command = "scp -r {}@{}:{} {}".format(hosts.get_host_item(host, 'user'), host['host'], path,
                                              dest if dest else os.path.dirname(path))
        sudopass = Responder(pattern=r'.*password:', response=hosts.get_host_item(host, 'pass') + '\n')
        hosts.execute(command, thread=True, other=other, out=True, hide=None, pty=True, watchers=[sudopass])

    else:
        """ scp
            1. 使用sshpass，主机需要先安装
                sshpass -p 111111 scp -r /opt/redis/ root@192.168.0.81:/tmp
    
            2. 使用Responder
        """
        for host in hosts.lists(index=False, other=other):
            user = hosts.get_host_item(host, "user")
            paww = hosts.get_host_item(host, "pass")
            command = "scp -r {} {}@{}:{}".format(path, user, host['host'],
                                                  dest if dest else os.path.dirname(path))
            if sshpass:
                c.run("sshpass -p {} {}".format(paww, command))
            else:
                sudopass = Responder(pattern=r'.*password:', response=paww + '\n')
                c.run(command, pty=True, watchers=[sudopass])


if __name__ == '__main__':
    from fabric import Config, Connection
    c = hosts.one()

    """ 测试方式：
            修改 init: config.install.source的值为无效值
    """
    def download_test(c):
        c.run("rm -rf /opt/redis; rm -rf /tmp/*redis*")

        print("\n======================== 指定local具体位置")
        download(c, "redis", source="http://download.redis.io/releases/redis-5.0.0.tar.gz",
                 local="/home/long/source/component/redis/redis-5.0.0.tar.gz")

        print("\n======================== 指定local的目录，自动搜索tar.gz、zip后缀")
        download(c, "redis", source="http://download.redis.io/releases/redis-5.0.0.tar.gz")

        print("\n======================== 指定local的目录，自动搜索tar.gz、zip后缀, 未给出source参数")
        download(c, "redis")

        print("\n======================== local 搜索失败，从网络下载")
        download(c, "redis", source="http://download.redis.io/releases/redis-5.0.0.tar.gz", local='/tmp')

    def copy_test(c):
        download(c, "redis")

        hosts.execute("rm /tmp/redis-5.0.0.tar.gz -rf", other=False)
        copy_pack(c, package(), '/tmp')

        hosts.execute("rm /tmp/redis-5.0.0.tar.gz -rf", other=True)
        copy_pack(c, package(), '/tmp', async=True)


    # download_test(c)
    # copy_test(c)

    copy_test(c)