from functools import reduce


def clean_axis(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])


def pipe(*funcs):
    def inner(arg):
        for f in funcs:
            arg = f(arg)
        return arg
    return inner
