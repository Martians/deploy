# coding=utf-8
from common import *

""" 多个配置合并起来
        1. 最低优先级是 config 目录中的配置，相当于默认配置
        2. 每个机器可以在复制 config 中目录中的相应配置到 ~ 下
"""
config = parse_config('network.yaml', merge=True, low='config')

def macbook():
    import platform
    return platform.system() == 'Darwin'


def initial_network(c, local):
    if local.flag.network:
        return
    else:
        local.flag.network = True

    if not config.segment:
        index = config.local.rfind('.')
        config.segment = config.local[:index]

    prepare_network(c)


def prepare_network(c, force=False):
    if not force and stdouted(c, 'ip address show | grep {bridge}'.format(bridge=config.bridge)):
        print('network already exist')
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
    """ 1. 数组：当做ip地址最后一段
        2. 字符：检查 config.address 部分是否存在相应的项目
    """
    if isinstance(host, int) or (isinstance(host, str) and host.isdigit()):
        return '{}.{}'.format(config.segment, host)

    elif config.address.get(host):
        return alloc(c, config.address.get(host))

    elif len(host) >= 2 and host[0] == 'h' and host[1:].isdigit():
        """ 用于 cluster，启动多个host，超过手动配置的个数 
        """
        base = int(config.address.get('h1'))
        return alloc(c, str(base + (int(host[1:]) - 1)))
    else:
        return host


def alloc_next(host, inc):
    """ 将传入的host的最后一部分（必须是全数字）加一

        alloc_next('10', 10)
        alloc_next('192.168.0.10', 10)
        alloc_next('h-10', 10)
        alloc_next('h10', 10)
    """
    import re
    host = str(host)
    match = re.search('[0-9]*$', host)
    result = match.group(0)
    if result:
        index = host.find(result)
        if index != -1:
            newh = host[:index] + str(int(result) + inc)
            return newh
    print('can not alloc next for host [{}]'.format(host))
    exit(-1)


def address(c, name, host, local):
    initial_network(c, local)

    host = alloc(c, host)
    print('set [name] host {host}'.format(host=host, name=name))

    """ 为了减少不必要信息，这里设置了 hide=True
    """
    c.run('sudo pipework {device} {name} {host}/{subnet}@{gateway}'
          .format(name=name, host=host, subnet=config.subnet, device=config.device,
                  bridge=config.bridge, gateway=config.gateway), warn=True, echo=False, hide=True)
    local.flag.host = host
