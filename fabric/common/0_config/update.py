# coding=utf-8

""" grep


    sed
        http://www.cnblogs.com/edwardlost/archive/2010/09/17/1829145.html
        sed 所有情况下输出都是0，除非语法错误; 如果使用此方法，必须检查output


"""
import os


class Update:
    config = os.getcwd() + '/conf_file'
    # conn = 0

    def conn(self, c):
        return c if c else self.conn

    def file(self, file):
        return file if file else self.config

    def init(self, c, file):
        return self.conn(c), self.file(file)

    def run():
        return {'warn': True, 'hide': True}


update = Update()
run = {'warn': True, 'hide': True}
# run = update.run()


def grep_line(c=None, data=None, file=None, **kwargs):
    c, file = update.init(c, file)

    if True:
        command = "sed -n '/{data}/=' {file}".format(data=data.replace('/', '\/'), file=file)
    else:
        command = "sed -n '$=' {file}".format(file=file)

    result = c.run(command, **run)
    output = result.stdout

    print("grep_line: {command}, line: {index}".format(command=command, index=output.replace('\n', ' ')))
    if len(output):
        if output.count('\n'):
            return int(output.split("\n")[0]), result
        else:
            return int(output), result
    else:
        return -1, None

if __name__ == '__main__':
    from fabric import Connection
    c = Connection('127.0.0.1')

    def test_grep_line():
        grep_line(c, 'num.io.threads=8')
        grep_line(c, '/mnt/abc')            # 特殊字符 /，需要转义


    test_grep_line()