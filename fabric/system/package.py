# coding=utf-8

from common.init import *
import common.hosts as hosts


def package(type='common', single='', centos=True):
    list = {'common': 'psmisc',
            'compile': 'gcc make',
            'java': 'java-1.8.0-openjdk-devel',
    }
    if centos:
        return 'yum install -y {} {}'.format(list[type], single)
    else:
        return ''


def install(type='common', single='', c=None, centos=True):
    command = package(type=type, single=single, centos=centos)
    if c:
        c.run(command, hide=None, pty=True)
    else:
        hosts.execute(command, hide=None, pty=True)




