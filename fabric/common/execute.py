# coding=utf-8

import common.hosts as hosts


def output_result(result, prefix="", work=""):
    """ 输出执行结果

        对stdout、stderr进行输出调整
    """
    if result.failed:
        failed = result.stderr.strip()
        failed = failed if failed else ""
        print("{0}<{1.connection.host}> {2}{1.stdout} {3}".format(prefix, result, work, failed))
    else:
        output = result.stdout.strip()
        print("{0}<{1.connection.host}> {2}{3}".format(prefix, result, work, output))


def multi(c, commands, go_on=False, hide=None):
    """ 多行命令
        1. 传入大字符串，依次执行每一行，判断每一行的执行结果；此函数采用此方式
        2. 传入大字符串，一次性传递给remote执行，对简单的一系列命令，可采用此方式

        处理逻辑：
        1. 可设计的参数
            1. 是否输出output、stderr
            2. 是否继续执行

        2. 最终选择：增加太多参数比较麻烦，简化：
            1. stderr：命令执行过程中不抛出异常（warn=True），执行完成后手动打印出来
            2. stdout：使用默认的方式进行，即会输出output到屏幕
    """
    index = -1
    failc = 0

    commands = commands.split('\n')
    for line in commands:
        index += 1
        line = line.strip()

        if line:
            result = c.run(line, warn=True, hide=hide)
            if result.failed:
                failc += 1
                output_result(result, prefix="\t==== line {} - ".format(index), work='- [{}]'.format(line))
                if not go_on:
                    print("\nmulti command, exit on {}/{}\n".format(index, len(commands)))
                    return
    if failc:
        print("\nmulti command, failed {}, success {}/{}\n".format(failc, len(commands) - failc, len(commands)))
    else:
        print("\nmulti command, total {}\n".format(len(commands)))


def group(group, command, err=True, out=False, hide=None, pty=None):
    """ group
        1. stderr：命令执行过程中不抛出异常（warn=True），执行完成后手动打印出来
        2. stdout：根据默认配置，决定是否输出

        选项：
        1. err：是否允许err、以及是否输出执行错误内容
        2. out：是否在执行完成后，聚合输出 stdout

        设计：
        1. group方式，并执行多行命令
            1. 按命令进行循环：每行命令，在所有conn执行完之后，转到下一条；建议使用此方式，比较简单
            2. 按conn执行：每个conn执行完所有命令后，转到下一个conn；这种方式可以自行调用 execute.run，在外层使用串行循环
    """
    command = command.strip()
    results = group.run(command, warn=True, hide=hide, pty=pty)
    count = 0

    ''' 输出错误的结果
    '''
    if err:
        for connection, item in results.items():
            if item.failed: count += 1

    if count:
        print("\nexecute [{}], failed {}:".format(command, count))
        for connection, item in results.items():
            if item.failed:
                output_result(item, prefix="\t".format())
        print()
        exit(-1)
    else:
        print("\nexecute [{}] success".format(command))

    ''' 正确的执行结果也输出
    '''
    if out:
        for connection, item in results.items():
            if not item.failed:
                output_result(item, prefix='\t')
    return results


if __name__ == '__main__':
    from fabric import Config, Connection
    from common.init import *

    c = hosts.conn(0)
    g = hosts.group(thread=True)

    succ = '''pwd
       pwd'''

    fail = ''' pwd
        ls /bb
        pwd 
    '''

    def test_multi():
        multi(c, succ)
        multi(c, fail)
        multi(c, fail, go_on=True)

    def test_group():
        group(g, "pwd")                # 执行成功，不显示输出结果
        group(g, "pwd", out=True)      # 执行成功，也显示输出结果

        # group("ls /bb")           # 执行失败，程序退出
        group(g, "ls /bb", err=False)  # 执行失败也继续

        group(g, "pwd", out=True)  # 串行执行，乱序返回

    def test_group_multi():
        group(g, succ)
        group(g, fail)

    test_multi()
    test_group()
