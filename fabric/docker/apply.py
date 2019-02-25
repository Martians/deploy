# coding=utf-8

import sys
from invoke import task
from common import *
import system
from docker.image import *
from docker import helps
from docker import network as net

@task
def clean(c, total=False, docker=False, image=False, resource=False):
    """ -di 删除所有docker、以及大部分image(保留centos、fabric); -t 删除所有image，并清理资源
    """
    if total:
        docker = True
        image = True
        resource = True

    """ total：清理全部，不保留任何image
        image: 删除image，保留ignore（但必须先清理相关docker）
    """
    if docker:
        clean_docker(c)

    if image:
        clean_image(c, total)

    if resource:
        clean_resource(c)

@task
def help(c):
    c = conn(c, True)
    system.help(c, '''
        docker history centos:base
        docker logs -f proxy
        docker images centos:test
        '''.format())

@task
def http(c, type=-1, port=local.http_port, path=local.http_path[0], update=False):
    """ 单独启动 http，可以指定更多参数; -u 更新仓库
    """
    start_http(c, type, port=port, path=path)
    helps.result(c, name='http', port=port)
    helps.repo(c)

    if update:
        """ 将proxy中得到的文件移动到http仓库目录，再执行 createrepo --update ...
        """
        c.run('docker exec http createrepo --update {}/{}'.format(local.http_path[1], local.http_url))

@task
def proxy(c, type=-1, path=local.proxy_path[0]):
    """ 单独启动 proxy，可以指定更多参数
    """
    start_proxy(c, type, path=path)
    helps.result(c, name='proxy', port=3142)
    helps.proxy(c, name='proxy')

@task
def sshd(c, type=-1, name='sshd', systemd=True, addr='sshd', enter=True):
    """ 基于sshd镜像，启动 sshd docker，默认使用 systemd
    """
    start_docker(c, type, name, base='sshd', exec='/bin/bash', systemd=systemd, host=addr, enter=enter)

@task
def cluster(c, name='sshd', systemd=True, count=3):
    """ 启动多个sshd docker
    """
    for i in range(1, count + 1):
        sshd(c, -1, name='{}-{}'.format(name, i), systemd=systemd, addr='h{}'.format(i), enter=False)

@task
def test(c, type=-1, name='test', base='sshd', port='', exec='/bin/bash', systemd=True, addr='test', enter=True):
    """ 构架测试场景

        1. 指定基础镜像：指定base生成纯净版本，可用于构建测试程序，可选项详见：prepare_images
           fab test --base centos:fabric --addr 100

        2. 内部执行安装：cd /fabric/docker; python3 server.py --server mariadb
    """
    start_docker(c, type, name, base=base, port=port, exec=exec, systemd=systemd, host=addr, enter=enter)

@task
def network(c, force=True):
    """ Todo：增加清理网络的代码
    """
    net.prepare_network(c, force=force)

@task
def mariadb(c, type=-1, name='', addr='db', enter=False):
    name = sys._getframe().f_code.co_name   # 这样其他构建server的函数都可以直接复制了
    sshd_server(c, type, name, host=addr, enter=enter)

@task
def postgres(c, type=-1, name='', addr='db', enter=False):
    name = sys._getframe().f_code.co_name
    sshd_server(c, type, name, host=addr, enter=enter)


if __name__ == '__main__':
    globing.invoke = True
    c = conn(hosts.one())

    # sshd(c, 1)
    # test(c)
    # http(c, type=0)
    # mariadb(c, 0)
