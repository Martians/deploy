# coding=utf-8

from invoke import task
from common import *
import system
from docker.image import *


@task
def install(c):
    build_images(c, local.base[0], local.base[1])

@task
def clean(c, all=False, docker=False, image=False, resource=False):
    if all:
        docker=True
        image=True
        resource=True

    if stdouted(c, 'docker images -q -f dangling=true'):
        color('clear dangling images!')
        c.run('docker rmi -f $(docker images -q -f dangling=true)')

    if docker:
        if stdouted(c, 'docker ps -aq'):
            color('clean docker')
            c.run('docker rm -f  $(docker ps -aq)')
            # c.run('docker ps -a')
        else:
            color('no docker', False)

    if image:
        if stdouted(c, 'docker images -aq'):
            color('clean images')
            c.run('docker rmi -f $(docker images -aq)')
            # c.run('docker images -a')
        else:
            color('no image', False)

    if resource:
        color('clean volume')
        c.run('docker volume prune -f')

        color('clean network')
        c.run('docker network prune -f')
        # c.run('docker network ls')
        # c.run('docker volume ls')
#
# @task
# def proxy(c):

@task
def help(c):
    c = conn(c, True)
    system.help(c, '''
        docker history centos:base
        docker images centos:test
        '''.format())

@task
def http(c, type=-1, port=local.http_port, path=local.http_path[0]):
    """ 单独启动 http，可以指定更多参数
    """
    start_http(c, type, port=port, path=path)

@task
def proxy(c, type=-1, path=local.proxy_path[0]):
    """ 单独启动 proxy，可以指定更多参数
    """
    start_proxy(c, type, path=path)

@task
def sshd(c, type=-1):
    start_docker(c, type, 'sshd', enter=True, exec='/bin/bash')

@task
def test(c, type=-1, fabirc=True):
    """ 根据base生成的纯净版本
    """
    start_docker(c, type)

@task
def cc(c):
    clean_image(c)

if __name__ == '__main__':
    # sshd(hosts.one(), 0)
    globing.invoke = True
    clean_image(conn(hosts.one()), True)