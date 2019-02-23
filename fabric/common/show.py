# coding=utf-8


def color(string, type='green', newline=True, fetch=False):
    color_map = {'red': 31, 'green': 32 }
    type = type if type in color_map else 'green'

    display = "{newline}\033[1;{color};40m{string}\033[0m"\
        .format(string=string, color=color_map.get(type), newline='\n' if newline else '')

    if fetch:
        return display
    else:
        print(display)


def color_partial(string, type='green', range=(0, 1)):
    print('{prefix}{string}{suffix}'.format(prefix=string[0:range[0]], suffix=string[range[1]:],
                                            string=color(string[range[0]:range[1]], type=type, fetch=True, newline=False)))


def color_sub(string, sub, type='green'):
    index = string.find(sub)
    color_partial(string, type=type, range=(index, index + len(sub)))


def color_re(string, partten, group=1, type='read'):
    import re
    match = re.search(partten, string, flags=0)
    result = match.group(group)

    if result:
        color_sub(string, result, type='red')
        return 1
