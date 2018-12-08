# coding=utf-8

import common.hosts as hosts


def output_result(result, prefix="", work=""):

    if result.failed:
        failed = result.stderr.strip()
        failed = failed if failed else ""
        print("{0}<{1.connection.host}> {2}{1.stdout} {3}".format(prefix, result, work, failed))
    else:
        output = result.stdout.strip()
        print("{0}<{1.connection.host}> {2}{3}".format(prefix, result, work, output))


def multi(c, commands, go_on=False, hide=None):
    ''' 执行多行命令
            1. 是否输出output、stderr
            2. 是否继续执行

        增加太多参数比较麻烦，简化：
            1. 不直接抛出异常，而是整理格式后，打印出来
            2. 使用默认的方式进行 output
    '''
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


def group(command, err=True, out=False, hide=None, thread=True):
    ''' group 执行
        1. 方便查看结果：为了方便查看出错的host：实际执行时不直接退出（传递给run warn=True），在后边统一手动输出结果
        2. 多条执行时：
            1) 按命令进行循环：每行命令，在所有conn执行完之后，转到下一条；使用此方式
            2) 按conn执行：每个conn执行完所有命令后，转到下一个conn；这种方式可以自行调用 execute.run，在外层使用串行循环

        选项：
        1. stderr：是否关注、以及是否输出执行错误内容
        2. stdout：是否输出正确内容
    '''
    command = command.strip()
    results = hosts.group(thread=thread).run(command, warn=True, hide=hide)
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
    from fabric import Config
    config = Config()
    hosts.parse_info(config, config.user, config.connect_kwargs.password)
    c = hosts.conn(0)

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
        group("pwd")                # 执行成功，不显示输出结果
        group("pwd", out=True)      # 执行成功，也显示输出结果

        # group("ls /bb")           # 执行失败，程序退出
        group("ls /bb", err=False)  # 执行失败也继续

        group("pwd", thread=False, out=True)  # 串行执行，乱序返回


    def test_group_multi():
        group(succ)
        group(fail)

    test_multi()
    test_group()