# coding=utf-8

""" grep


    sed
        http://www.cnblogs.com/edwardlost/archive/2010/09/17/1829145.html
        sed 所有情况下输出都是0，除非语法错误; 如果使用此方法，必须检查output


"""
import os


class Update:
    file = 'conf_file'
    test = True

    if test:
        # 监测到erro是否退出
        err_exit = False

    path = os.path.join(os.getcwd(), file)
    cache = ''
    conn = 0

    def _conn(self, c):
        return c if c else self.conn

    def _path(self, file):
        return file if file else self.path

    def init(self, c, file):
        return self._conn(c), self._path(file)

    def run():
        return {'warn': True, 'hide': True}


update = Update()
run = {'warn': True, 'hide': True}
# run = update.run()


def arg(kwargs, name):
    return kwargs[name] if name in kwargs else ''


""" sed
        sed -n '/.*LOCAL_JMX/p' conf_file 
"""

def grep_line(c, data=None, file=None, **kwargs):
    """ kwargs：
            grep：使用grep进行搜索，不需要进行转义
    """
    c, file = update.init(c, file)

    """ 处理：
            有数据，查找数据所在行
            无数据，查找最后一行
            
        命令：
            grep -n 'data' file      
            sed  -n '/data/=' file    /需要转义为\/;     
    """
    if data:
        if kwargs.get('grep'):
            command = "grep -n '{prefix}{data}' {file}".\
                format(data=data, file=file, prefix=arg(kwargs, 'prefix'))
        else:
            command = "sed -n '/{prefix}{data}/=' {file}".\
                format(data=data.replace('/', '\/'), file=file, prefix=arg(kwargs, 'prefix'))
    else:
        command = "sed -n '$=' {file}".format(file=file)

    result = c.run(command, **run)
    output = result.stdout.strip()

    print("grep_line: {command}, line: [{index}]".format(command=command, index=output.replace('\n', ' ')))
    if len(output):
        """ 返回值：
                grep: line:text, 需要再次 split
                sed:  line
        """
        find = output.split("\n")
        return int(find[0].split(':')[0]), len(find)
    else:
        return -1, 0


def sed(c, name, command, file):
    if update.test:
        print("[{name}]: sed {command} {file}".format(name=name, command=command, file=update.file))
        command = 'cat {file} | sed {command}'.format(command=command, file=file)
        result = c.run(command, **run)
        update.output = result.stdout
        return result
    else:
        return c.run('sed -i {command} {file}'.format(command=command, file=file), **run)


def dump(c, key, search, count=0):
    print("----------- {key}, output: {count}".format(key=key, count=abs(count)))
    result = c.run('''echo '{cache}' | grep -{type} {count} '{search}' '''
          .format(cache=update.output, type='A' if count >= 0 else 'B', count=abs(count), search=search), **run)

    update.recent = result.stdout
    print("[debug]:\n{}".format(update.recent))
    return result.stdout


def appand(c, data, locate=None, file=None, pos=0, **kwargs):
    """ 参数：
            data: 要插入的完整数据
            locate：data插入的位置

        说明：
            1. data 存在多个匹配，不进行处理
            2.
    """
    c, file = update.init(c, file)

    """ 要添加的数据已经存在
            1. 在指定位置出现：与locate的位置进行比较
            2. locate不存在：不需要再检查是否进行插入
            3. locate存在，但相对位置不匹配，继续执行
    """
    index, count = grep_line(c, data, file, **kwargs)
    if count > 1:
        print("append: data [{}] exist multi [{}]".format(data, count))
        return exit(-1) if update.err_exit else False

    elif index != -1:
        spos = 1 if pos == 0 else pos

        if locate:
            key_line, count = grep_line(c, locate, file, **kwargs)
            if count > 1:
                print("append: data exist [{}], not append".format(count))
                return exit(-1) if update.err_exit else False

            if key_line + spos == index:
                print("appand: [{data}] already exist, line: {index}".format(data=data, index=index))
                return False
            elif key_line == -1:
                print("appand: [{data}] already exist, line: {index}, locate not exist".format(data=data, index=index))
                return False
        else:
            print("append: [{data}] already exist, locate none, success".format(data=data))
            return True
    """ 定位到要插入数据的位置
    """
    index, count = grep_line(c, locate, file, **kwargs)
    if count > 1:
        print("grep_line: locate exist [{}]".format(count))
        return exit(-1) if update.err_exit else False
    elif index == -1:
        index = grep_line(c, file)[0]
    else:
        index += pos if pos <= 0 else pos - 1

    command = "'{index}a\{data}'".format(index=index, data=data)
    result = sed(c, 'append', command, file=file)

    dump(c, data, data, -(1 if pos == 0 else pos))
    return result.ok


if __name__ == '__main__':
    from fabric import Connection
    c = Connection('127.0.0.1')

    def segment(info):
        print("\n##########################################################################")
        print("======================== {info}:".format(info=info))

    def check(v1, v2):
        if v1 != v2:
            c.run('''echo '{}' > /tmp/v1; echo '{}' > /tmp/v2'''.format(v1, v2))
            c.run('diff /tmp/v1 /tmp/v2', warn=True)
            exit(-1)

    def match(v):
        check(v.strip('\n'), update.recent.strip('\n'))

    def test_grep_line():
        """ 找到所有数据
        """
        segment("no prefix search")
        check(grep_line(c, 'num.io.threads=8')[1], 2)
        check(grep_line(c, '/mnt/abc')[1], 1)            # 特殊字符 /，需要转义

        check(grep_line(c, 'num.io.threads=8', grep=True)[1], 2)
        check(grep_line(c, '/mnt/abc', grep=True)[1], 1)

        """ 精确定位一条
        """
        segment("prefix search")
        check(grep_line(c, 'num.io.threads=8', prefix='^')[1], 1)
        check(grep_line(c, '/mnt/abc', prefix='^', grep=True)[1], 1)


    def test_append():
        if 1:
            """ 数据不存在
            """
#             check(appand(c, 'append_line', 'LOCAL_JMX=yes'), True)
#             match('''
#     LOCAL_JMX=yes
# append_line''')

            """ 数据已经存在
                    1. 存在多个
                            不进行处理：可以增加数定位的精确度
            """
            check(appand(c, 'LOCAL_JMX'), False)

            """     2. 存在一个，none locate
                            为了从多个中精确定位一个，grep时使用prefix
            """
            check(appand(c, 'LOCAL_JMX', prefix='$'), True)

            """     3. 存在一个，有 locate
                        
            """cd 
            # check(appand(c, 'LOCAL_JMX=no'), False)

        # 插入到尾部：给出了locate，但没找到
        # check(appand(c, 'append_line', 'not_exit_line'), True)

        # # 插入到尾部：未给出locate
        # check(appand(c, 'append_line', 'not_exit_line'), True)

        # if 1:
#             """ locate 有多个匹配
#             """
#             check(appand(c, 'append_line', 'LOCAL_JMX'), False)
#
#             """ 增加locate的匹配前缀
#             """
#             check(appand(c, 'append_line', '^LOCAL_JMX', grep=True), True)
#             match('''
# LOCAL_JMX=no
# append_line''')


        # 插入到某行之上的第三行
        # check(appand(c, 'append_line', 'LOCAL_JMX=yes', -3), True)

        # 数据已经存在，不需要插入

        # 数据已经存在，但是不符合与locate的位置关系

        # 数据已经存在，符合与locate的位置关系

# test_grep_line()
    test_append()