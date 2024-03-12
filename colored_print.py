"""指导输出彩色的文字"""
import builtins as __builtin__
from random import choice


class FrequentlyUsedColors:
    """存放各种颜色的代码"""
    RED = '\u001b[38;5;196m'
    BLUE = '\u001b[38;5;12m'
    GREEN = '\u001b[38;5;46m'
    YELLOW = '\u001b[38;5;220m'
    CYAN = '\u001b[38;5;51m'
    PINK = '\u001b[38;5;213m'
    MAGENTA = '\u001b[38;5;163m'
    OLIVE = '\u001b[38;5;100m'
    GRAY = '\u001b[38;5;240m'
    DARKGRAY = '\u001b[38;5;235m'
    RESET = '\u001b[0m'
    COLORS = [RED, BLUE, GREEN, YELLOW, CYAN, PINK, MAGENTA, OLIVE, GRAY,
              DARKGRAY, RESET]


def color_print(*args, color='default'):
    """调用这个函数可以在stdout中打印对应色彩的文字"""
    args = [str(item) for item in args]
    s = " ".join(args)

    if color in ['default', 'black', 'k', 0]:
        s = FrequentlyUsedColors.RESET + s
    elif color in ['blue', 'b', 1]:
        s = FrequentlyUsedColors.BLUE + s
    elif color in ['cyan', 'c', 2]:
        s = FrequentlyUsedColors.CYAN + s
    elif color in ['gray', 'grey', 9]:
        s = FrequentlyUsedColors.GRAY + s
    elif color in ['darkgrey', 'darkgray', 10]:
        s = FrequentlyUsedColors.DARKGRAY + s
    elif color in ['green', 'g', 3]:
        s = FrequentlyUsedColors.GREEN + s
    elif color in ['magenta', 'm', 4]:
        s = FrequentlyUsedColors.MAGENTA + s
    elif color in ['red', 'r', 5]:
        s = FrequentlyUsedColors.RED + s
    elif color in ['yellow', 'y', 6]:
        s = FrequentlyUsedColors.YELLOW + s
    elif color in ['pink', 7]:
        s = FrequentlyUsedColors.PINK + s
    elif color in ['olive', 'o', 8]:
        s = FrequentlyUsedColors.OLIVE + s
    elif color in ['random', 'rand']:
        s = choice(FrequentlyUsedColors.COLORS) + s
    elif color in ['discrete_random', 'drand']:
        s = ''.join(list(map(lambda x: choice(FrequentlyUsedColors.COLORS) +
                             x + FrequentlyUsedColors.RESET, s)))
    else:
        raise TypeError
    s += FrequentlyUsedColors.RESET
    return __builtin__.print(s)


def red_print(*args):
    """red"""
    return color_print(*args, color='red')


def blue_print(*args):
    """blue"""
    return color_print(*args, color='blue')


def cyan_print(*args):
    """cyan"""
    return color_print(*args, color='cyan')


def gray_print(*args):
    """gray"""
    return color_print(*args, color='gray')


def darkgrey_print(*args):
    """darkgrey"""
    return color_print(*args, color='darkgrey')


def green_print(*args):
    """green"""
    return color_print(*args, color='green')


def magenta_print(*args):
    """magenta"""
    return color_print(*args, color='magenta')


def yellow_print(*args):
    """yellow"""
    return color_print(*args, color='yellow')


def pink_print(*args):
    """pink"""
    return color_print(*args, color='pink')


def olive_print(*args):
    """olive"""
    return color_print(*args, color='olive')


def random_print(*args):
    """random color"""
    return color_print(*args, color='random')
