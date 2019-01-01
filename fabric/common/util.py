# coding=utf-8


def sep(full, data, sep=','):
    if not full:
        full = data
    else:
        full = full + sep + data
    return full
