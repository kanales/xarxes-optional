from functools import reduce


def pipe(*funcs):
    def inner(arg):
        for f in funcs:
            arg = f(arg)
        return arg
    return inner
