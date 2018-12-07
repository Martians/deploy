# coding=utf-8


valid_item = ['name', 'host', 'user', 'pass', 'port', 'disk']

# 按照加入的顺序列出的host
host_array = []
host_index = {}
host_local = {}

''' 解析配置文件
    1. 建立索引：使用下方配置例子：192.168.0.80
        1. first  ：'local' => host          字符串
        2. host ip：'192.168.0.80' => host   字符串
        3. last ip：'80' => host             字符串（如果没有冲突时，自动添加为索引）
        4. index  ：'0'  => host、0 => host  字符串、数字
       
    2. 配置说明 
        1. 使用方式：
            1）用户密码
                默认密码：使用fabric配置 user、connect_kwargs、password
                单独密码：hosts.list.host['pass']
                
            3）服务配置：
                默认配置：hosts.[name].[item]
                单独配置：hosts.list.host[item name]
            
    3. 常见错误：
        1. pass设置为数字，而不是字符串
---
     hosts:
         list:
           - name: local
             host: 192.168.0.80
             user: root
             pass: '111111'             # 必须是字符串
             
           - host: 192.168.0.82
             disk: /mnt/d1,/mnt/d2      # 获取hosts[1]的disk时，将获得此信息
             name:                      # value为空，不会建立这个索引
           
           - host: 192.168.0.83
         
         disk:                          # 获得默认 disk时，将array内容合并成字符串
           - /mnt/disk1
           - /mnt/disk2
'''
def parse_info(config, user=None, paww=None):
    parse_host(config.hosts)

    import copy
    global host_local
    host_local = copy.copy(config.hosts)
    del host_local['list']

    if user: host_local['user'] = user
    if paww: host_local['pass'] = paww

def parse_host(hosts):
    index = 0
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

        ''' 添加index、ip last
        '''

        host['index'] = index
        index += 1
        host_array.append(host)
        add_host_index(host['host'], host)

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


def list_host(array=True, index=True, other=True):
    # https://docs.python.org/3/library/pprint.html
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
    '''
        1. key 为字符串：name、host、ip last
        2. key 作为整数：根据编号进行查找
    '''
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

    from _ctypes import Array

    if isinstance(data, Array) or isinstance(data, list):
        data = sep.join(data)
    return data


def get_item(index, name, sep=","):
    host = get_host(index)
    return get_host_item(host, name, sep)

def lists(index=True, other=False):
    return [host['index'] if index else host
            for host in host_array
            if not other or host is not host_array[0]]

def group(thread=True):
    name = 'thread_group' if thread else 'group'
    if name not in host_local:
        host_local.name = ThreadingGroup() if thread else Group()
        host_local.name.extend([conn(index) for index in lists()])
    return host_local.name

def execute(command, thread=True, err=True, output=False):
    results = group(thread=thread).run(command, warn=True, hide=True)

    count = 0
    if err:
        for connection, item in results.items():
            if item.failed: count += 1

    if count:
        print("execute [{}], failed count <{}>:".format(command, count))

        for connection, item in results.items():
            if item.failed:
                failed = item.stderr.strip()
                print("\t<{0.host}> {1.stdout}{2}".format(connection, item, failed if failed else ""))
        print()
    else:
        print("execute [{}] success".format(command))

    if output:
        for connection, item in results.items():
            if not item.failed:
                print("\t<{0.host}> {1}".format(connection, item.stdout.strip()))
    return results

#######################################################################################################################
from fabric import Connection, SerialGroup as Group, Config, ThreadingGroup


def conn(data):

    ''' 建立到某个host的连接
            可以指定 ip最后一位、name
    '''
    host = get_host(data)

    if 'conn' not in host:
        user = get_host_item(host, 'user')
        port = get_host_item(host, 'port')
        passwd = get_host_item(host, 'pass')
        kwarg = {'password': passwd} if passwd else None
        host['conn'] = Connection(host=host['host'], user=user, port=port, connect_kwargs=kwarg)
    return host['conn']


if __name__ == '__main__':
    config = Config()
    parse_info(config, config.user, config.connect_kwargs.password)
    list_host()

    def test_host_info():
        # host
        print(get_host("192.168.0.82")['host'])

        # name
        print(get_host("local")['host'])

        # ip last
        print(get_host("82")['host'])

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

    def test_group():
        group().run("hostname")
        group(False).run("hostname")
        execute("ls /bb", thread=True)
        execute("ls /bb", thread=False)

        execute("pwd", output=True)

    test_host_info()
    test_host_item()
    test_get_host()
    test_get_list()
    test_group()
