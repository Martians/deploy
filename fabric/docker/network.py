# coding=utf-8
from common import *

config = load_yaml('network.yaml')
config = config.network


def initial_network(c, local):
    if local.flag.network:
        return
    else:
        local.flag.network = True

    if not config.segment:
        index = config.local.rfind('.')
        config.segment = config.local[:index]

    prepare_network(c)


def prepare_network(c):
    if stdouted(c, 'ip address show | grep {bridge}'.format(bridge=config.bridge)):
        print('network exist')
        return

    color('create network')

    local = '{local}/{subnet}'.format(local=config.local, subnet=config.subnet)
    c.run('''sudo ip addr del {network} dev {device}
sudo ip link add link {device} dev {bridge} type macvlan mode bridge
sudo ip link set {bridge} up
sudo ip addr add {network} dev {bridge}
sudo route add default gw {gateway}	'''
          .format(network=local, subnet=config.subnet, device=config.device, bridge=config.bridge, gateway=config.gateway))


def alloc(c, host):
    if isinstance(host, int) or (isinstance(host, str) and host.isdigit()):
        return '{}.{}'.format(config.segment, host)

    elif config.address.get(host):
        return alloc(c, config.address.get(host))

    else:
        return host


def address(c, name, host, local):
    initial_network(c, local)
    host = alloc(c, host)

    print('set [name] host {host}'.format(host=host, name=name))
    c.run('sudo pipework {device} {name} {host}/{subnet}@{gateway}'
          .format(name=name, host=host, subnet=config.subnet, device=config.device,
                  bridge=config.bridge, gateway=config.gateway), warn=True)
    local.flag.host = host