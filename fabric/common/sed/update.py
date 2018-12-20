# coding=utf-8

from common.sed.append import *


def grep_data(c, key, data=None, file=None, **kwargs):
    c, file = local.init(c, file)

    """ 多行处理时，将\n转换为其他字符
    """
    def multi(data):
        more = ''
        if data and data.count('\n'):
            data = data.replace('\n', local.multi)
            more = "sed ':a; N; s/\\n/{}/g; ta;' | ".format(local.multi)
        return data, more
    data, more = multi(data)

    command = grep_param(key, data, **kwargs)

    result, command = grep(c, 'grep_data', command, file, more=more)
    output = result.stdout.strip('\n')
    print("[grep_data]: {command} {file}, line: [{output}]".format(command=command, file=local.file(file), output=output))
    return True if len(output) else False


def update(c, key, data, file,
           check=None, **kwargs):
    """ kwargs:
            grep: grep时相关参数
            sed:  sed时相关参数
    """
    c, file = local.init(c, file)
    check = local.check(check)

    if check.get("pre") and \
       grep_data(c, key, **kwargs):
        print("update, item {} already exist".format(grep_param(key, data, **kwargs)))
        return 1

    command = sed_param(key, data, **kwargs)

if __name__ == '__main__':
    from fabric import Connection

    c = Connection('127.0.0.1')
    enable = False

    def initial(info, cache):
        local.initial(cache)
        print("\n########################################################################## {}", format(info))


    def output(info):
        print("\n--------------------------------------------------------------------------- {info}:".format(info=info))


    def check(v1, v2):
        """ 数据写入到文件后用diff比较
        """
        if v1 != v2:
            c.run('''echo '{}' > /tmp/v1; echo '{}' > /tmp/v2'''.format(v1, v2), echo=False)
            c.run('diff /tmp/v1 /tmp/v2', warn=True)
            exit(-1)

    def match(v):
        check(v.strip('\n'), local.result.strip('\n'))

    def test_grep_data():
        initial("grep", """
UsePAM yes
# one logical cluster from joining another.
data_file_directories:
    - /mnt/disk1
    - /mnt/disk2
    - /mnt/disk3
""")
        if enable or True:
            output("key value not exist")
            check(grep_data(c, 'UsePAM', 'no'), False)

            output("key value exist")
            check(grep_data(c, 'UsePAM', 'yes'), True)

            output("key value exist, value multi line")
            check(grep_data(c, 'data_file_directories', '''
    - /mnt/disk1
    - /mnt/disk2
    - /mnt/disk3''', grep={'sep': ':'}), True)

            output("key value exist, print 1")
            check(grep_data(c, 'UsePAM', 'yes', show=1), True)

            output("key value exist, print 0")
            check(grep_data(c, 'UsePAM', 'yes', show=0), True)

    def test_update():
        initial("update", """
UsePAM yes

    # Ex: "<ip1>,<ip2>,<ip3>"LOCAL_JMX=yes
    - seeds: 192.168.10.1
    
# Setting listen_address to 0.0.0.0 is always wrong.
# ss
listen_address: 192.168.10.1

data_file_directories: 
    - /mnt/disk1
    - /mnt/disk2
    - /mnt/disk3
""")

        if enable or True:
            output("data not exist")

            output("data not exist, need prefix to find only one")

            output("data not exist, key not the head")
            output("data not exist, key not the head")

            output("data not exist, key is multi line")

            output("data exist, ignore")

    test_grep_data()