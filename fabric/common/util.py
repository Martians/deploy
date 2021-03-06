# coding=utf-8


class Dict(dict):
    def __setattr__(self, k, v):
        self[k] = v

    def __getattr__(self, k):
        value = self.get(k)
        if isinstance(value, dict):
            value = Dict(value)
        return value

    def withdraw(self):
        """ 删除第一级 Key，通常只用于第一级只有一个Key的情况
        """
        temp = {}
        for (key, data) in self.items():
            if not isinstance(data, dict):
                continue
            for (k, v) in data.items():
                temp[k] = v
        self.clear()
        self.update(temp)

    def updating(self, other):
        """ 像遍历文件路径一样进行遍历
        """
        curr = merge(self, other)
        self.update(curr)

    def dict(self):
        """ 返回原始 dict；类Dict某些地方实现不好，在一些场景下使用失败
        """
        return merge('', self, origin=True)


def merge(a, b, origin=False):
    if not a:
        a = dict() if origin else Dict()

    for k, v in b.items():
        if isinstance(v, dict):
            a[k] = merge(a.get(k), v, origin)
        else:
            a[k] = v
    return a


def sep(full, data, sep=','):
    """ 构建full：第一次添加data时，不加sep分隔符
    """
    if not full:
        full = str(data)
    elif data:
        full = full + sep + str(data)
    return full


def args(name, prefix='', suffix='', ignore=False):
    """ name 为空时，返回空值
        name 有值时，添加前缀后缀后返回
    """
    if name:
        return prefix + ('' if ignore else str(name)) + suffix
    else:
        return ''


def args_default(name, defaults):
    """ 参数为空，则返回默认值
    """
    return name if name else defaults


def args_distill(list, kwargs):
    """ filter：从kwargs中，提取list中关注的几个参数
    """
    dict = {}
    for item in list.split(','):
        item = item.strip(' ')
        if item and item in kwargs:
            dict[item] = kwargs.pop(item)
    return dict


def args_insert(kwargs, **update):
    """ default：如果update中的参数，在kwargs未设置，就添加进去
    """
    for (d, v) in update.items():
        if d not in kwargs:
            kwargs[d] = v
    return kwargs


def stdouted(c, cmd, out=False):
    """ 执行命令产生stdout时，则返回 True
    """
    stdout = c.run(cmd, echo=False, hide=True, warn=True).stdout.strip()
    if out:
        return stdout
    else:
        return len(stdout) > 0


def macos():
    import platform
    return platform.system() == 'Darwin'


def macos_show(display=''):
    if macos():
        if display:
            print(display)
        return True
    else:
        return False


def macos_work(linux='', mac=''):
    return mac if macos() else linux