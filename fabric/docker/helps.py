# coding=utf-8

from invoke import task
from common import *
import system


def sshd(c, name, host='127.0.0.1', info=False):
    if info:
        color('ssh clean cache [client side]:')
        print('''    rm ~/.ssh/known_hosts -f
or,
    echo "StrictHostKeyChecking=no" > ~/.ssh/config
    echo "UserKnownHostsFile=/dev/null" >> ~/.ssh/config
''')
        """ docker 内部，网卡名称是 eth1
        """
        print('''show host address:''')
        c.run('docker exec {name} ip addr show eth1 | grep inet | grep [0-9.].*/ --color'.format(name=name))

    else:
        print('''enter host:
        docker exec -it {name} /bin/bash
        ssh root@{host}'''.format(host=host, name=name))
