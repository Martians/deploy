# coding=utf-8

from invoke import task
from common import *
import system


def sshd(c, name, host='127.0.0.1', sshd=False):
    if sshd:
        color('ssh clean cache [client side]:')
        print('''    rm ~/.ssh/known_hosts -f
or,
    echo "StrictHostKeyChecking=no" > ~/.ssh/config
    echo "UserKnownHostsFile=/dev/null" >> ~/.ssh/config
''')

    else:
        print('''\nenter host:
        docker exec -it {name} /bin/bash
        ssh root@{host}'''.format(host=host, name=name))


def result(c, name, port=False, host=True, **kwargs):
    """ docker建立成功后，显示结果
            1. docker 内部，网卡名称是 eth1
    """
    if port:
        c.run('sudo netstat -antp | grep :$PORT[\t\ ] --color')
    else:
        print('''show host address:''')
        c.run('    docker exec {name} ip addr show eth1 | grep inet | grep [0-9.].*/ --color'.format(name=name))