# coding=utf-8

from fabric import Connection, SerialGroup as Group, Config, ThreadingGroup


class Host(dict):
    def __init__(self, hosts, *args, **kw):
        self.hosts = hosts
        dict.__init__(self, *args, **kw)

    def __setattr__(self, k, v):
        self[k] = v

    def __getattr__(self, k):
        # return self.get(k)
        return self.item(k, '')

    @classmethod
    def __item(cls, host, name):
        item_dict = {'name' : lambda: host.host.split('.')[-1]}
        func = item_dict.get(name)
        return func() if func else None

    def item(self, name, sep=',', defv=''):
        if name in self:
            data = self[name]

        elif self.__item(self, name):
            data = self.__item(self, name)

        elif name in hosts.other:
            data = hosts.other[name]

        elif defv:
            data = defv
        else:
            return None

        if sep:
            from _ctypes import Array
            if isinstance(data, Array) or isinstance(data, list):
                data = sep.join(data)
        return data

class Hosts:
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
    valid = ['name', 'host', 'user', 'pass', 'port', 'disk', 'type']

    control = {}
    array = []
    index = {}
    other = {}

    def parse(self, config, user=None, paww=None):
        self.parse_host(config)

        """ 获取配置中lists之外的部分
        """
        import copy
        self.other = copy.copy(config)
        del self.other['list']

        """ 保存默认账号、密码
        """
        if user: self.other['user'] = user
        if paww: self.other['pass'] = paww

    def parse_host(self, hosts):
        index = 0
    
        for item in hosts['list']:
            host = Host(self, item.copy())
            if 'host' not in host:
                print("parse host, [host] not in {}".format(host))
                exit(-1)

            for key in item:
                ''' 检查是否有name字段，有的话就添加索引
                      并在host删除这个信息，简化调试信息
                '''
                if key == 'name' and item[key]:
                    self.add_index(item[key], host)
                    # del host[key]

                elif key not in self.valid:
                    print("parse host, [{}] in {} not valid".format(key, host))
                    exit(-1)

            if host.get('type') == 'control':
                self.control = host
                host.index = -1
                self.add_index(host.type, host)
            else:
                ''' 添加index、ip last exceed host cou
                        '''
                host.index = index
                index += 1

                self.array.append(host)
                self.add_index(host.host, host)

        """ control 节点也是普通节点，普通节点也使用control中配置的密码等信息
        """
        if self.control:
            for index in range(len(self.array)):
                if self.array[index]['host'] == self.control['host']:
                    self.array[index] = self.control
                    self.control['index'] = index
        else:
            self.control = self.array[0]
            self.add_last()

    def add_index(self, name, host):
        if name in self.index:
            print("name {} already regist, as: {}".format(name, self.index[name]))
            exit(-1)
        self.index[name] = host

    def add_last(self):
        for host in self.array:
            ip = host.host.split('.')[-1]
            if ip in self.index:
                print("add_host_ip_last, but last part: {} already registed", ip)
                return

        for host in self.array:
            ip = host.host.split('.')[-1]
            self.add_index(ip, host)

    ########################################################################################################################
    def dump(self, array=True, index=True, other=True):
        """ 用于debug

            https://docs.python.org/3/library/pprint.html
        """
        import pprint
        if array:
            # pprint.pprint(self.host_array)
            pp = pprint.PrettyPrinter(indent=4)
            print("host list:")
            pp.pprint(self.array)

        if index:
            print("\nhost dict:")
            pp.pprint(self.index)

        if other:
            print("\nhost info:")
            pp.pprint(self.other)
        print()

    def get_host(self, index):
        if isinstance(index, Host):
            return index
        elif isinstance(index, Connection):
            index = index.host

        """ 根据任何索引，获取host

            1. key 为字符串：name、host、ip last
            2. key 作为整数：根据编号进行查找
        """
        if index in self.index:
            return self.index[index]

        else:
            # 本来应该传入数字，但是这里传入了字符串，转换为index
            if isinstance(index, str):
                if index.isdigit():
                    index = int(index)

                elif index == self.one(True)['host']:
                    """ 通过 host 地址查找，查找的是control
                    """
                    return self.one(True)

            if isinstance(index, int):
                if index >= 0 and index <= len(self.array):
                    return self.array[index]
                else:
                    print("host_info: index {} exceed host count: {}".format(index, len(self.array)))
                    exit(-1)
            else:
                print("host_info: key {} not exist".format(index))
                exit(-1)

    def item(self, index, name, sep=",", defv=''):
        host = self.get_host(index)
        return host.item(name, sep, defv)

    ########################################################################################################################
    def is_master(self, host):
        return host.index == 0

    def lists(self, index=True, other=False, count=0):
        return [host.index if index else host
                for host in self.array
                if not other or not self.is_master(host)
                if count == 0 or host.index < count]

    def conns(self, other=False):
        return [self.conn(index) for index in self.lists(other=other)]

    def group(self, thread=True, other=False, conns=None):

        if conns is not None:
            """ 将临时传入的连接列表，组成 Group
            """
            host_conns = ThreadingGroup() if thread else Group()
            host_conns.extend(conns)
            return host_conns
        else:
            name = 'thread_group' if thread else 'group'
            if name not in self.other:
                self.other[name] = ThreadingGroup() if thread else Group()
                self.other[name].extend([self.conn(index) for index in self.lists(other=other)])
            return self.other[name]

    def execute(self, command, groups=None, thread=True, err=True, out=False, hide=True, other=False, go_on=False,**kwargs):
        groups = self.group(thread=thread, other=other, conns=groups)

        import common.execute as execute
        return execute.group(groups, command, err=err, out=out, hide=hide, go_on=go_on, **kwargs)

    def group_filter(self, command, reverse=False, other=False, conn=True):
        results = self.execute(command, err=False, other=other)
        list = []
        for connect, result in results.items():
            if result.ok ^ reverse:
                if conn:
                    list.append(connect)
                else:
                    list.append(get_host(connect.host))
        return list
    #######################################################################################################################

    def one(self, host=False):
        return self.get_host('control') if host else self.conn('control')

    def conn(self, data):
        """ 建立到某个host的连接，并保存下来
                可以指定 ip最后一位、name、host、index等
        """
        host = self.get_host(data)

        if 'conn' not in host:
            passwd = host.item('pass')
            kwarg = {'password': passwd} if passwd else None
            host.conn = Connection(host=host.host, user=host.user, port=host.port, connect_kwargs=kwarg)
        return host.conn


hosts = Hosts()


if __name__ == '__main__':
    config = Config()
    hosts.parse(config.hosts, config.user, config.connect_kwargs.password)
    # import common.init
    hosts.dump()

    def test_host_info():
        host = hosts.array[1]

        # host
        print(hosts.get_host(host.host).host)

        # name
        print(hosts.get_host("local").host)

        # ip last, '82'
        # last = host.host.split('.')[-1]
        # print(hosts.get_host(last).host)

        # index
        print(hosts.get_host(1).host)

        # index：字符串
        print(hosts.get_host('1').host)

        # wrong
        # print(host_info("109").host)

    def test_host_item():
        print(hosts.item(0, "disk", ':'))
        print(hosts.item(1, "disk", ':'))

    def test_get_host():
        hosts.conn(0).run("hostname")
        hosts.conn(1).run("hostname")

    def test_get_list():
        print(hosts.lists())
        print(hosts.lists(other=True, index=False))

    def test_get_item():
        print(hosts.item('control', 'pass'))
        print(hosts.item(1, 'pass'))
        print(hosts.item(1, 'user'))

    def test_group():
        print("\nserial:")
        hosts.group().run("hostname")

        print("\nasync:")
        hosts.group(False).run("hostname")

        # print("\nslave:")
        # group(other=True).run("hostname")

    def test_group_filter():
        import common.disk as disk
        print(hosts.group_filter(disk._file_exist_command('/root/test')))

        print(hosts.group_filter(disk._file_exist_command('/root/test'), reverse=True))

    test_host_info()
    test_host_item()
    test_get_host()
    test_get_list()
    test_get_item()
    test_group()
    test_group_filter()

