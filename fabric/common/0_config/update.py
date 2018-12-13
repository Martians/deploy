# coding=utf-8

""" grep


    sed
        http://www.cnblogs.com/edwardlost/archive/2010/09/17/1829145.html
        sed 所有情况下输出都是0，除非语法错误; 如果使用此方法，必须检查output


"""


class Update:
    file = 'config'


update = Update()


def grep_line(c, file=None, data=None):
    """ 找到data所在的行号
    """
    if data:
        command = "sed -n '/{key}/=' {file}".format(key=data, file=file)
    else:
        command = "sed -n '$=' {file}".format(file=file)

    result = c.run(command, warn=True, hide=True)
    output = result.stdout

    print("grep_line: {command}, line: {index}".format(command=command, index=output))
    if len(output):
        if output.count('\n'):
            return int(output.split("\n")[0]), result
        else:
            return int(output), result
    else:
        return -1, None

