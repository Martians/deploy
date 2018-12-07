# coding=utf-8

'''
    更多方法：https://blog.csdn.net/ialexanderi/article/details/79021312
'''
def file_exist(c, path, name=None, dir=False):
    ''' 精确名字查找
    '''
    flag = 'd' if dir else 'f'
    name = '*' + name + '*' if name else ""
    return c.run("[ -{} {}/{} ]".format(flag, path, name), warn=True).ok


def file_search(c, path, name=None, dir=False):
    ''' 模糊名字查找
    '''
    flag = 'd' if dir else '^d'
    result = c.run("ls -l {} | grep ^[{}] | awk '{{print $9}}' | grep {}".format(path, flag, name), warn=True)

    # split('\n')[:-1]
    fileList = result.stdout.strip().split('\n')
    if len(fileList) == 1:
        return fileList[0]

    elif len(fileList) > 1:
        print("too much similar dir [{}] in {}: {}".format(name, path, fileList))
        exit(-1)
    return None