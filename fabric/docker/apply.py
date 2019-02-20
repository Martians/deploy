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
def sshd(c, type=-1):
    start_docker(c, type, 'http', port=80, enter=True)

@task
def test(c, type=-1, fabirc=True):
    """ 根据base生成的纯净版本
    """
    start_docker(c, type)


if __name__ == '__main__':
    sshd(hosts.one())