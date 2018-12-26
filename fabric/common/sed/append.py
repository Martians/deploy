# coding=utf-8

from common.sed.config import *

""" sed -n '/.*LOCAL_JMX/p' config.properties

    grep：使用grep进行搜索，不需要进行转义
            sed： =、/ 需要转义
"""

""" 多行处理时，将\n转换为其他字符
"""
def grep_multi(data):
    head = ''
    if data and data.count('\n'):
        data = data.replace('\n', local.multi)
        head = "sed ':a; N; s/\\n/{}/g; ta;' |".format(local.multi)
    return data, head


def grep_param(key, data, options, quote=True, for_sed=False):
    """ 此处没有进行 grep的参数转换，在外部进行转换
            1. 可以在此处进行转换，但是在sed_param
    """
    if not for_sed:
        key = local.grep_fix(key)
        data = local.grep_fix(data)

    hasdata = '{grep[sep]}{grep[more]}{data}'.format(grep=options, data=data)
    command = "{raw}{show}{quote}{grep[prefix]}{key}{grep[suffix]}{data}{quote}".\
        format(raw=arg(options, 'raw', True), show=local.show_option(options.get('show')),
               grep=options, key=key, data=hasdata if data else '', quote="'" if quote else '')
    return command


def sed_param(key, data, options):
    """ 1. 与grep不同，这里search时，不使用固定data，而是用.*一类的，这样才能替换掉
        2. data如果包括多行，进行转换；也仅是在此处转换
    """
    search = local.sed_fix(grep_param(key, None, options, quote=False, for_sed=True))
    search = '{search}{grep[sep]}{grep[more]}{grep[loc_data]}'.format(search=search, grep=options)

    result = '{sed[rep_prefix]}{key}{sed[sep]}{data}'.format(key=key, data=local.sed_fix(data, False), sed=options)
    command = 's{sed[tag]}{search}{sed[tag]}{result}{sed[tag]}{sed[end]}'.format(
                search=search, result=result, sed=options)
    return command, search, result


def do_grep(c, name, command, file, options):
    head = arg(options, 'head', True)
    if options.get('sed'):
        command = 'sed {command}'.format(command=command)
    else:
        command = 'grep {command}'.format(command=command)

    """ 在执行任务之前输出，通常调试时用到
    """
    local.debug_command('do_grep', '{command} {file}'.format(name=name, command=command, file=local.file(file)))

    if local.test:
        # print('''echo '{}' | {}{}'''.format(local.cache, arg(options, 'head', True), command))
        result = c.run('''echo '{}' | {}{}'''.format(local.cache, head, command), **local.run)
    else:
        if head:
            """ 多行情况：head的末尾包含了一个 |, 需要去掉
            """
            head = head.split('|')[0] # print('''{} {} | {}'''.format(head, file, command))
            result = c.run('''{} {} | {}'''.format(head, file, command), **local.run)
        else:
            local.check_param(file)
            result = c.run('''{} {}'''.format(command, file), **local.run)

    local.grep_out = result.stdout.strip('\n')
    local.debug_output('grep output', local.grep_out)
    return result, command


def do_sed(c, name, command, file, options):
    command = "sed {flag}'{command}'".format(flag='' if local.test else '-i ', command=command, file=local.file(file))

    """ 在执行任务之前输出，通常调试时用到
    """
    local.debug_command('do_sed', '{command} {file}'.format(name=name, command=command, file=local.file(file)))

    if local.test:
        result = c.run('''echo '{}' | {}'''.format(local.cache, command), **local.run)
        local.sed_out = result.stdout
        local.debug_output('sed output', local.sed_out)
    else:
        """ 这里使用的是sed -i, 因此没有输出结果，不获取 local.sed_out
        """
        local.check_param(file)
        result = c.run('{command} {file}'.format(command=command, file=file), **local.run)

    print('[{name}]: {command} {file}'.format(name=name, command=command, file=local.file(file)))
    if result.failed:
        print("do sed, but failed, err: [{}]".format(result.stderr.strip('\n')))
        exit(-1)
    return result


def dump(c, key, search=None, count=0, file=None):
    print("----------- {key}, context: {count}".format(key=search if search else key, count=abs(count)))
    command = '''grep {show}'{search}' '''.format(show=local.show_option(count), search=local.grep_fix(search))

    if local.test:
        command = '''echo '{cache}' | {command} '''.format(cache=local.sed_out, command=command)
    else:
        command = '''{command} {file}'''.format(command=command, file=file)

    local.debug_command('dump info', '\n{command} {file}'.format(command=command, file=local.file(file)))

    result = c.run(command, **local.run)
    if result.failed and len(result.stderr) > 0:
        print("dump sed output failed, command:\n {}\n {}{}".format(command, result.stdout, result.stderr))

    local.result = result.stdout.strip('\n')

    """ 此处强制输出，并且另外使用一行
    """
    local.debug_output('debug', local.result, line=True, force=True, seperate='\n')
    return result.stdout


def grep_line(c, data=None, file=None, **kwargs):
    """ kwargs：
    """
    c, file = local.init(c, file)

    kwargs['for_append'] = True
    options = local.grep_option(**kwargs)

    data, head = grep_multi(data)
    options['head'] = head

    if data:
        """ 处理：
                有数据，查找数据所在行
                无数据，查找最后一行
            命令：
                grep -n 'data' file      
                sed  -n '/data/=' file    /需要转义为\/;     
        """
        if options.get('sed'):
            data = local.sed_fix(data)
            command = "-n '/{prefix}{data}/='".format(data=data, prefix=arg(options, 'prefix'))
        else:
            data = local.grep_fix(data)
            command = "-n '{prefix}{data}'".format(data=data, prefix=arg(options, 'prefix'))
    else:
        if kwargs.get('grep'):
            command = '-c'
        else:
            command = "-n '$='".format()

    result, command = do_grep(c, 'grep_line', command, file, options)
    output = result.stdout.strip()
    print("[grep_line]: {command} {file}, line: [{index}]".
          format(command=command, file=local.file(file), index=output.replace('\n', ' ').split(':')[0]))

    if len(output):
        """ 返回值：
                grep: line:text, 需要再次 split
                sed:  line
        """
        find = output.split("\n")
        return int(find[0].split(':')[0]), len(find)
    else:
        return -1, 0


def append(c, data, locate=None, file=None, pos=1, **kwargs):
    """ 参数：
            data: 要插入的完整数据
            locate：data插入的位置

        说明：
            1. data 存在多个匹配，不进行处理
            2.
    """
    c, file = local.init(c, file)

    """ 前提：data 已经存在
            1. 在指定位置出现：与locate的位置进行比较
            2. locate不存在： 不需要再检查是否进行插入
            3. locate存在：  但相对位置不匹配，继续执行
    """
    index, count = grep_line(c, data, file, **kwargs)
    if count > 1:
        print("[append]: data [{}] exist multi [{}], failed".format(data, count))
        return local.exit(False)

    elif index != -1:
        if locate:
            key_line, count = grep_line(c, locate, file, **kwargs)
            if key_line == -1:
                print("[append]: data [{}] already exist, line: {}, locate [{}] not exist".format(data, index, locate))
                return local.exit(False)
            elif count > 1:
                print("[append]: data [{}] already exist, locate [{}] exist count [{}]".format(data, locate, count))
                return local.exit(False)

            elif key_line + pos == index:
                print("[append]: data [{}] already exist, match with locate [{}], line: {}".format(data, locate, index))
                return True

            elif index == 1 and data.count('\n'):
                print("[append]: data [{}]\n  --- is multi line, no need check position, data already exist".format(data))
                return True
            else:
                print("[append]: data [{}] already exist, but locate [{}] not match, line: {}".format(data, locate, index))
        else:
            print("[append]: data [{data}] already exist, locate none, success".format(data=data))
            return True

    """ 定位到要插入数据的位置
    """
    index, count = grep_line(c, locate, file, **kwargs)
    on_the_end = False
    if count > 1:
        print("[append]: locate [{}] exist [{}], failed".format(locate, count))
        return exit(-1) if local.exit_on_err else False
    elif index == -1:
        index = grep_line(c, None, file)[0]
        on_the_end = True
    else:
        index += pos - 1 if pos > 0 else pos

    command = "{index}a\{data}".format(index=index, data=local.sed_fix(data, False))
    result = do_sed(c, 'append', command, file=file, options=local.sed_option(**kwargs))

    dump(c, data, locate, pos, file)

    if on_the_end:
        print("[append]: add [{data}] on line {index}, the end of the file, [{locate}] not exist"
              .format(data=data, index=index + 1, locate=locate))
    else:
        print("[append]: add [{data}] on line {index}, {pos} {type} [{locate}]"
              .format(data=data, index=index + 1, pos=abs(pos), type='after' if pos > 0 else 'before', locate=locate))
    return local.exit(result.ok)


if __name__ == '__main__':
    c = test_mode(True)
    enable = False

    def test_grep_line(use_sed):
        initial('test grep', """
listen_address: 192.168.10.1

num.io.threads=8
/mnt/abc

# set broadcast_rpc_address to a value other than 0.0.0.0.
#   num.io.threads=8
    - /mnt/disk1
    - /mnt/disk2
    - /mnt/disk3
""")
        if enable or True:
            output("search key, exist 2")
            check(grep_line(c, 'num.io.threads=8', grep={'sed': use_sed})[1], 2)

            output("search key, exist only 1, have special char")
            check(grep_line(c, '/mnt/abc', grep={'sed': use_sed})[1], 1)    # 特殊字符 /，使用sed需要转义

            output("search key, use prefix search, locate only 1")
            check(grep_line(c, 'num.io.threads=8', grep={'prefix': '^', 'sed': use_sed})[1], 1)

            output("search key, multi line")
            check(grep_line(c, '''
    - /mnt/disk1
    - /mnt/disk2
    - /mnt/disk3''', grep={'sed': use_sed})[1], 1)

    ###################################################################################################################
    def test_append():
        initial("test append", """
if [ "x$LOCAL_JMX" = "x" ]; then
bbc=3
    LOCAL_JMX=yes
fi
LOCAL_JMX=no
cc_address: 192.168.10.11""")

        if enable or True:
            output("data not exist, insert pos = 1")
            check(append(c, 'append_line', 'LOCAL_JMX=yes'), True)
            match('''
    LOCAL_JMX=yes
append_line''')

            output("data not exist, insert pos = -2")
            check(append(c, 'append_line', '    LOCAL_JMX=yes', pos=-2), True)
            match('''
append_line
bbc=3
    LOCAL_JMX=yes''')
            output("data not exist, location have multi")
            check(append(c, 'append_line', 'LOCAL_JMX'), False)

            output("data not exist, location not find")
            check(append(c, 'append_line', 'not_exist_location'), True)

            output("data not exist, locate not set, append to end")
            check(append(c, 'append_line'), True)

            ###########################################################################################################
            output("data exist, but multi data, not process")
            check(append(c, 'LOCAL_JMX'), False)

            output("data exist, although multi data, but use prefix for grep, no need insert")
            check(append(c, 'LOCAL_JMX', grep={'prefix': '$'}), True)

            output("data exist, location exist, position match")
            check(append(c, 'LOCAL_JMX=no', 'cc_address: 192.168.10.11', pos=-1, grep={'sed': True}), False)

            output("data exist, location exist, position not match, insert again")
            check(append(c, 'LOCAL_JMX=no', 'cc_address: 192.168.10.11'), True)
            match('''
cc_address: 192.168.10.11
LOCAL_JMX=no''')

            output("data exist, location have multi")
            check(append(c, 'LOCAL_JMX=no', 'LOCAL_JMX'), False)

    test_grep_line(False)
    test_grep_line(True)
    test_append()