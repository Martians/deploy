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

    path = os.path.join(os.getcwd(), file)
    cache = ''

    # conn = 0

    def conn(self, c):
        return c if c else self.conn

    def path(self, file):
        return file if file else self.path

    def init(self, c, file):
        return self.conn(c), self.path(file)

    def run():
        return {'warn': True, 'hide': True}


update = Update()
run = {'warn': True, 'hide': True}
# run = update.run()


def arg(kwargs, name):
    return kwargs[name] if name in kwargs else ''


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

    print("grep_line: {command}, line: {index}".format(command=command, index=output.replace('\n', ' ')))
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


def dump(c, key, search, line=0):
    if line == 0:
        result = c.run("echo {cache} | grep -{type} {count} '{search}' "
                   .format(cache=update.cache, type='A' if line > 0 else 'B',
                           search=search, count=abs(line)), **run)
    else:
        print("----------- {key}, line: {line}".format(key=key, line=line))
        result = c.run("echo {cache} | grep -{type} {count} '{search}' "
              .format(cache=update.cache, type='A' if line > 0 else 'B', count=abs(line), search=search))
    update.recent = result.stdout
    return result.stdout


def appand(c, data, locate=None, file=None, pos=0, **kwargs):
    """ data: 要插入的完整数据
        locate：data插入的位置
    """
    c, file = update.init(c, file)

    """ 要添加的数据已经存在
    """
    index = grep_line(c, data, file, **kwargs)[0]
    if index != -1:
        """ 检查是否在指定的位置
        """
        spos = 1 if pos == 0 else pos

        key_line = grep_line(c, locate, file, **kwargs)[0]
        if key_line + spos == index:
            print("appand: [{data}] already exist, line: {index}".format(data=data, index=index))
            return False, None
        elif key_line == -1:
            print("appand: [{data}] already exist, line: {index}, locate not exist".format(data=data, index=index))
            return False, None

    """ 找到locate所在的行
    """
    index = grep_line(c, locate, file, **kwargs)[0]
    if index == -1:
        index = grep_line(file)[0]
    else:
        index += pos if pos <= 0 else pos - 1

    command = "'{index}a\{data}'".format(index=index, data=data)
    result = sed(c, 'append', command, file=file)
    dump(c, data, 0)
    return result.ok, result


if __name__ == '__main__':
    from fabric import Connection
    c = Connection('127.0.0.1')

    def segment(info):
        print("\n##########################################################################")
        print("======================== {info}:".format(info=info))

    def check(v1, v2):
        assert(v1 == v2)

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
        appand(c, 'append_line', 'LOCAL_JMX=yes')

    # test_grep_line()
    test_append()