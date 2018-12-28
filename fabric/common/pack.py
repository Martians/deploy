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
    local = local if local else default_config['source']['source']

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
    default_config['source']['source'] = file_path


def package(parent=None):
    """ 获得安装包的路径
    """
    path = default_config['source']['source']
    if parent:
        file = os.path.basename(path)
        return os.path.join(parent, file)
    else:
        return path


def copy_pack(c, path=None, dest=None, check=True, sshpass=False, other=False, async=True):
    path = path if path else package()
    dest = dest if dest else os.path.dirname(path)

    remote = os.path.join(dest, os.path.basename(path))

    if check:
        """ 找到hosts, 这些hosts上该包不存在
        """
        import common.disk as disk
        groups = hosts.group_filter(disk._file_exist_command(remote), reverse=True, other=other)
    else:
        groups = hosts.group(thread=False, other=other)

    if async:
        """ 异步线程方式执行，需要已经设置了免密码登陆
        """
        host = hosts.get_host(c.host)
        command = "scp -r {}@{}:{} {}".format(hosts.get_host_item(host, 'user'), host['host'], path, dest)
        sudopass = Responder(pattern=r'.*password:', response=hosts.get_host_item(host, 'pass') + '\n')
        hosts.execute(command, groups=groups, thread=True, other=other, out=True, hide=None, pty=True, watchers=[sudopass])

    else:
        """ scp
            1. 使用sshpass，主机需要先安装
                sshpass -p 111111 scp -r /opt/redis/ root@192.168.0.81:/tmp
    
            2. 使用Responder
        """
        for host in hosts.lists(index=False, other=other):
            ignore = True
            for conn in groups:
                """ 如果是需要发送的连接，那么group中执行命令，已经让 host['conn'] 有了值
                """
                if 'conn' in host and conn is host['conn']:
                    ignore = False
                    break
            if ignore:
                print("copy_pack, host [{}] already exist source".format(host['host']))
                continue

            scp(c, host, path=path, dest=dest, sshpass=sshpass)

    if len(groups) == 0:
        print("\ncopy_pack complete, [{}] already exist on all hosts, ignore".format(remote))
    else:
        print("\ncopy_pack complete, copy [{}] to [{}] host".format(remote, len(groups)))


def scp(c, host, path, dest=None, sshpass=False):
    dest = dest if dest else os.path.dirname(path)

    user = hosts.get_host_item(host, "user")
    paww = hosts.get_host_item(host, "pass")
    command = "scp -r {} {}@{}:{}".format(path, user, host['host'], dest)

    if sshpass:
        c.run("sshpass -p {} {}".format(paww, command))
    else:
        sudopass = Responder(pattern=r'.*password:', response=paww + '\n')
        c.run(command, pty=True, watchers=[sudopass])


def unpack(c, name, path=None, parent=None):
    parent = parent if parent else default_config['source']['parent']
    path = path if path else package()

    if file_exist(c, parent, name, dir=True):
        print("unpack, source path [{}/{}] already exist".format(parent, name))
        return 1

    """ 解压到 path下，名称可能带有版本号

        path下不能存在任何包含 name 的文件夹，否则无法判断哪个是解压出来后的目录
    """

    c.run("mkdir -p {}".format(parent))
    if not file_actual(c, parent, name, dir=True):
        print("unpack source [{}] ...".format(path))

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


if __name__ == '__main__':
    from fabric import Config, Connection
    c = hosts.one()

    """ 测试方式：
            修改 init: config.source.source的值为无效值
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
        print("\n======================== copy source, and set source() value")
        download(c, "redis")

        if 1:
            print("\n======================== copy to all host, sync")
            hosts.execute("rm /tmp/redis-5.0.0.tar.gz -rf")
            copy_pack(c, package(), '/tmp', async=False)

            print("\n======================== copy to slave, async")
            hosts.execute("rm /tmp/redis-5.0.0.tar.gz -rf")
            copy_pack(c, package(), '/tmp', async=True, other=True)

            print("\n======================== copy to all host, sync, not check")
            copy_pack(c, package(), '/tmp', async=False, check=False)

            print("\n======================== copy to all host, async, not check")
            copy_pack(c, package(), '/tmp', async=True, check=False)

        if 1:
            print("\n====== prepare")
            hosts.execute("rm /tmp/redis-5.0.0.tar.gz -rf")
            copy_pack(c, package(), '/tmp', other=True, async=False)
            print("\n======================== copy to slave, sync, already exist, no need copy")
            copy_pack(c, package(), '/tmp', other=True, async=False)

            print("\n====== prepare")
            hosts.execute("rm /tmp/redis-5.0.0.tar.gz -rf")
            copy_pack(c, package(), '/tmp', other=True)
            print("\n======================== copy to slave, async, already exist, no need copy")
            copy_pack(c, package(), '/tmp', other=True)

            print("\n====== prepare")
            hosts.execute("rm /tmp/redis-5.0.0.tar.gz -rf")
            copy_pack(c, package(), '/tmp', async=False, other=True)
            print("\n======================== copy to all, async, slave already have pack, only copy to master")
            copy_pack(c, package(), '/tmp', async=False)

    def unpack_test(c):
        download(c, "redis")

        print("\n======================== unpack")
        c.run("sudo rm -rf /opt/redis")
        unpack(c, 'redis')

        print("\n======================== unpack but exist ")
        unpack(c, 'redis')

    download_test(c)
    copy_test(c)
    unpack_test(c)