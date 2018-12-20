# coding=utf-8

import sys, os
import time

sys.path.append(os.path.join(os.getcwd(), "../.."))

from invoke import task
from common.init import *
from common.pack import *

import common.hosts as hosts
import common.sed as sed

file = '/tmp/start.sh'
home = '/home/guijichaxun/SimpleBenchmark_1216'

@task
def make(c, servers, clients, mode, round, thread, max):
    write(c, "")
    write(c, "")
    write(c, "")
    write(c, 'echo "============================================"')
    write(c, 'echo "{}c {}s {}t"'.format(len(clients.split(',')), len(servers.split(',')), thread))


    zookeeper = '-z 192.168.108.1:24002/kafka -b 192.168.108.124:21005 -p newlocation_1'
    prefix = 'java -cp {home}/target/lib/*:{home}/target/SimpleBenchmark.jar'.format(home=home)
    suffix = '>/dev/null 2>&1 &'

    write(c, "UUID=`date +%s`")
    write(c, "sh {}/tests/killallivylite.sh".format(home))
    server_command = '''{prefix} cn.nimblex.ivylite.CommunicationTrackServer -c {home}/config/example-ivylite-server.xml {suffix}'''.format(home=home, prefix=prefix, suffix=suffix)

    slist = ''
    for server in servers.split(','):
        write(c, '''ssh {} "{}" &'''.format(server, server_command))
        slist += ('_' if slist else '') + server.split('.')[-1]

    write(c, 'sleep 200')

    client_command = '''{prefix} cn.nimblex.ivylite.CommunicationTrackWithKafkaStream -c {home}/config/example-ivylite-consumer.xml {zookeeper} -r {max} -g ${{UUID}} -m {mode} -t {thread} -l {home}/tests/testKafka/results/2brokers_200partitions/{mode}/{clients}c{servers}s{thread}t'''.format(home=home,
               prefix=prefix, suffix=suffix, zookeeper=zookeeper, max=max, mode=mode, thread=thread, round=round, clients=len(clients.split(',')), servers=len(servers.split(',')))

    for cip in clients.split(','):
        write(c, '''ssh {cip} "{client_command}/node{slist}/{round}/node{last}" &'''.format(cip=cip, client_command=client_command, last=cip.split('.')[-1],
                                                                                            slist=slist, round=round, suffix=suffix))
    write(c, "wait")

    c.run("cat {}".format(file))

def write(c, command):
    c.run('''echo -E '{}' >> {}'''.format(command, file))


c = hosts.one()
c.run("rm -rf {}".format(file))
make(c, '192.168.108.17,192.168.108.18,192.168.108.19,192.168.108.20,192.168.108.104,192.168.108.105,192.168.108.118,192.168.108.122', '192.168.108.17,192.168.108.18,192.168.108.19,192.168.108.20,192.168.108.104,192.168.108.105,192.168.108.118,192.168.108.122', 'one-by-one', 1, 25, 30)
make(c, '192.168.108.17,192.168.108.18,192.168.108.19,192.168.108.20,192.168.108.104,192.168.108.105,192.168.108.118,192.168.108.122', '192.168.108.17,192.168.108.18,192.168.108.19,192.168.108.20,192.168.108.104,192.168.108.105,192.168.108.118,192.168.108.122', 'one-by-one', 1, 25, 30)

make(c, '192.168.108.17,192.168.108.18,192.168.108.19,192.168.108.20', '192.168.108.104,192.168.108.105,192.168.108.118,192.168.108.122', 'one-by-one', 1, 50, 15)
make(c, '192.168.108.104,192.168.108.105,192.168.108.118,192.168.108.122', '192.168.108.17,192.168.108.18,192.168.108.19,192.168.108.20', 'one-by-one', 1, 50, 15)

make(c, '192.168.108.17,192.168.108.18,192.168.108.19', '192.168.108.20,192.168.108.104,192.168.108.105,192.168.108.118,192.168.108.122', 'one-by-one', 1, 40, 15)
make(c, '192.168.108.104,192.168.108.105,192.168.108.118', '192.168.108.17,192.168.108.18,192.168.108.19,192.168.108.20,192.168.108.122', 'one-by-one', 1, 40, 15)

make(c, '192.168.108.17,192.168.108.104,192.168.108.105,192.168.108.118,192.168.108.122', '192.168.108.18,192.168.108.19,192.168.108.20', 'one-by-one', 1, 67, 15)
make(c, '192.168.108.17,192.168.108.18,192.168.108.19,192.168.108.20,192.168.108.104', '192.168.108.105,192.168.108.118,192.168.108.122', 'one-by-one', 1, 67, 15)

make(c, '192.168.108.19,192.168.108.20,192.168.108.104,192.168.108.105,192.168.108.118,192.168.108.122', '192.168.108.17,192.168.108.18', 'one-by-one', 1, 100, 15)
make(c, '192.168.108.17,192.168.108.18,192.168.108.19,192.168.108.20,192.168.108.118,192.168.108.122', '192.168.108.104,192.168.108.105', 'one-by-one', 1, 100, 15)

make(c, '192.168.108.17,192.168.108.18,192.168.108.19', '192.168.108.18,192.168.108.19,192.168.108.20', 'one-by-one', 1, 67, 15)
make(c, '192.168.108.104,192.168.108.105,192.168.108.118', '192.168.108.105,192.168.108.118,192.168.108.122', 'one-by-one', 1, 67, 15)

make(c, '192.168.108.17,192.168.108.18', '192.168.108.19,192.168.108.20,192.168.108.104,192.168.108.105,192.168.108.118,192.168.108.122', 'one-by-one', 1, 34, 15)
make(c, '192.168.108.104,192.168.108.105', '192.168.108.17,192.168.108.18,192.168.108.19,192.168.108.20,192.168.108.118,192.168.108.122', 'one-by-one', 1, 34, 15)

make(c, '192.168.108.17,192.168.108.18', '192.168.108.18,192.168.108.19,192.168.108.20', 'one-by-one', 1, 67, 10)
make(c, '192.168.108.104,192.168.108.105', '192.168.108.105,192.168.108.118,192.168.108.122', 'one-by-one', 1, 67, 10)

make(c, '192.168.108.17', '192.168.108.18,192.168.108.19,192.168.108.20', 'one-by-one', 1, 67, 5)
make(c, '192.168.108.104', '192.168.108.105,192.168.108.118,192.168.108.122', 'one-by-one', 1, 67, 5)

make(c, '192.168.108.17,192.168.108.18', '192.168.108.19,192.168.108.20', 'one-by-one', 1, 100, 10)
make(c, '192.168.108.104,192.168.108.105', '192.168.108.118,192.168.108.122', 'one-by-one', 1, 100, 10)

make(c, '192.168.108.17', '192.168.108.20', 'one-by-one', 1, 200, 15)
make(c, '192.168.108.104', '192.168.108.122', 'one-by-one', 1, 200, 15)





# @task
# def total(c, mode):
#     for m in mode:
#         make(c)