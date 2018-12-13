# coding=utf-8

valid_item = ['name', 'host', 'user', 'pass', 'port', 'disk', 'type']

""" 
    1. 按照index序号
    2. 相关字符串索引
    3. 其他配置内容，主要是host默认配置，如disk等
    
"""
host_conf = {}
host_one = {}

host_array = []
host_index = {}
host_local = {}


""" 解析配置

    1. 建立索引：使用下方配置例子中的：192.168.0.80
        1. first  ：'local' => host          字符串
        2. host ip：'192.168.0.80' => host   字符串
        3. last ip：'80' => host             字符串（如果没有冲突时，自动添加为索引）
        4. index  ：'0'  => host、0 => host  字符串、数字
       
    2. 配置说明 
        1. 使用方式：
            1）用户密码
                默认密码：使用fabric配置 user、connect_kwargs、password
                单独密码：hosts.list.host['pass']
                
            2）服务配置：
                默认配置：hosts.[name].[item]
                单独配置：hosts.list.host[item name]
                
            3）节点类型：
                控制节点：type = control; 控制节点也可以是普通host，但需要再写一遍
                其他节点：
                
            4）节点分组：尚未实现
                每个节点可以属于多个分组
            
    3. 常见错误：
        1. pass设置为数字，而不是字符串
---
     hosts:
         list:
           - name: local
             host: 192.168.0.80
             user: root
             pass: '111111'             # 如果都由数字组成，则必须是字符串
             type: control              # 指定控制节点，该节点不计入index的count
           
           - host: 192.168.0.80         # 控制节点同时也是host之一
             
           - host: 192.168.0.82
             disk: /mnt/d1,/mnt/d2      # 获取hosts[1]的disk时，将获得此信息
             name:                      # value为空，不会建立这个索引
           
           - host: 192.168.0.83
         
         disk:                          # 获得默认 disk时，将array内容合并成字符串
           - /mnt/disk1
           - /mnt/disk2
"""


def parse_info(config, user=None, paww=None):
    parse_host(config.hosts)

    global host_conf
    host_conf = config

    import copy
    global host_local
    host_local = copy.copy(config.hosts)
    del host_local['list']

    if user: host_local['user'] = user
    if paww: host_local['pass'] = paww


def parse_host(hosts):
    index = 0
    global host_one
    for item in hosts.list:
        host = item.copy()
        if 'host' not in host:
            print("parse host, [host] not in {}".format(host))
            exit(-1)

        for key in item:
            ''' 检查是否有name字段，有的话就添加索引
                  并在host删除这个信息，简化调试信息
            '''
            if key == 'name' and item[key]:
                add_host_index(item[key], host)
                del host[key]

            elif key not in valid_item:
                print("parse host, [{}] in {} not valid".format(key, host))
                exit(-1)

        if 'type' in host and host['type'] == 'control':
            host_one = host
            host['index'] = -1
            add_host_index(host['type'], host)
        else:
            ''' 添加index、ip last exceed host cou
                    '''
            host['index'] = index
            index += 1

            host_array.append(host)
            add_host_index(host['host'], host)

    """ control 节点也是普通节点，普通节点也使用control中配置的密码等信息
    """
    if host_one:
        for index in range(len(host_array)):
            if host_array[index]['host'] == host_one['host']:
                host_array[index] = host_one
                host_one['index'] = index
    else:
        host_one = host_array[0]
    add_host_iplast()


def add_host_index(name, host):
    if name in host_index:
        print("name {} already regist, as: {}".format(name, host_index[name]))
        exit(-1)
    host_index[name] = host


def add_host_iplast():
    for host in host_array:
        ip = host['host'].split('.')[-1]
        if ip in host_index:
            print("add_host_ip_last, but last part: {} already registed", ip)
            return

    for host in host_array:
        ip = host['host'].split('.')[-1]
        add_host_index(ip, host)

########################################################################################################################


def dump(array=True, index=True, other=True):
    """ 用于debug

        https://docs.python.org/3/library/pprint.html
    """
    import pprint
    if array:
        # pprint.pprint(host_array)
        pp = pprint.PrettyPrinter(indent=4)
        print("host list:")
        pp.pprint(host_array)

    if index:
        print("\nhost dict:")
        pp.pprint(host_index)

    if other:
        print("\nhost info:")
        pp.pprint(host_local)
    print()


def get_host(index):
    """ 根据任何索引，获取host

        1. key 为字符串：name、host、ip last
        2. key 作为整数：根据编号进行查找
    """
    if index in host_index:
        return host_index[index]

    else:
        # 本来应该传入数字，但是这里传入了字符串，转换为index
        if isinstance(index, str):
            if index.isdigit():
                index = int(index)

        if isinstance(index, int):
            if index >= 0 and index <= len(host_array):
                return host_array[index]
            else:
                print("host_info: index {} exceed host count: {}".format(index, len(host_array)))
                exit(-1)
        else:
            print("host_info: key {} not exist".format(index))
            exit(-1)


def get_host_item(host, name, sep=","):
    if name in host:
        data = host[name]

    elif name in host_local:
        data = host_local[name]

    else:
        return None
        """ 对用户名和密码，在初始化时已经进行了设置
        """
        # if name in host_conf:
        #     data = host_conf[name]
        #
        # elif name == 'pass' and 'connect_kwargs' in host_conf \
        #         and 'password' in host_conf['connect_kwargs']['password']:
        #     data = host_conf['connect_kwargs']['password']
        # else:
        #     return None

    from _ctypes import Array
    if isinstance(data, Array) or isinstance(data, list):
        data = sep.join(data)
    return data


def get_item(index, name, sep=","):
    host = get_host(index)
    return get_host_item(host, name, sep)

########################################################################################################################

def is_master(host):
    return host['index'] == 0


def lists(index=True, other=False):
    return [host['index'] if index else host
            for host in host_array
            if not other or not is_master(host)]


def group(thread=True, other=False):
    name = 'thread_group' if thread else 'group'
    if name not in host_local:
        host_local.name = ThreadingGroup() if thread else Group()
        host_local.name.extend([conn(index) for index in lists(other=other)])
    return host_local.name


def execute(command, thread=True, err=True, out=False, hide=True, other=False, **kwargs):
    import common.execute as execute
    return execute.group(group(thread=thread, other=other),
                         command, err=err, out=out, hide=hide, **kwargs)

#######################################################################################################################
from fabric import Connection, SerialGroup as Group, Config, ThreadingGroup


def one(host=False):
    return get_host('control') if host else conn('control')


def conn(data):
    """ 建立到某个host的连接，并保存下来
            可以指定 ip最后一位、name、host、index等
    """
    host = get_host(data)

    if 'conn' not in host:
        user = get_host_item(host, 'user')
        port = get_host_item(host, 'port')
        passwd = get_host_item(host, 'pass')
        kwarg = {'password': passwd} if passwd else None
        host['conn'] = Connection(host=host['host'], user=user, port=port, connect_kwargs=kwarg)
    return host['conn']


if __name__ == '__main__':
    from common.init import *
    config = Config()
    parse_info(config, config.user, config.connect_kwargs.password)
    dump()

    def test_host_info():
        host = host_array[1]

        # host
        print(get_host(host['host'])['host'])

        # name
        print(get_host("local")['host'])

        # ip last, '82'
        last = host['host'].split('.')[-1]
        print(get_host(last)['host'])

        # index
        print(get_host(1)['host'])

        # index：字符串
        print(get_host('1')['host'])

        # wrong
        # print(host_info("109")['host'])

    def test_host_item():
        print(get_item(0, "disk", ':'))
        print(get_item(1, "disk", ':'))

    def test_get_host():
        conn(0).run("hostname")
        conn(1).run("hostname")

    def test_get_list():
        print(lists())
        print(lists(other=True, index=False))

    def test_get_item():
        print(get_item('control', 'pass'))
        print(get_item(1, 'pass'))
        print(get_item(1, 'user'))

    def test_group():
        print("\nserial:")
        group().run("hostname")

        print("\nasync:")
        group(False).run("hostname")

        # print("\nslave:")
        # group(other=True).run("hostname")

    # test_host_info()
    # test_host_item()
    # test_get_host()
    # test_get_list()
    # test_get_item()
    test_group()

