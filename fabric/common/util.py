# coding=utf-8


class Dict(dict):
    def __setattr__(self, k, v):
        self[k] = v

    def __getattr__(self, k):
        return self.get(k)


def sep(full, data, sep=','):
    if not full:
        full = data
    else:
        full = full + sep + data
    return full


def args_fil(list, kwargs):
    """ 只保留关注的几个参数, filter
    """
    dict = {}
    for item in list.split(','):
        item = item.strip(' ')
        if item and item in kwargs:
            dict[item] = kwargs.pop(item)
    return dict


def args_def(kwargs, **update):
    """ 如果参数中未设置，就增加默认值配置
    """
    for (d, v) in update.items():
        if d not in kwargs:
            kwargs[d] = v
    return kwargs
