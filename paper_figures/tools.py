#!/usr/bin/env python3

import math
import os
import os.path
import pathlib
import platform
import random
from shutil import copyfile

import matplotlib
import matplotlib.pyplot
import numpy
from matplotlib.ticker import FuncFormatter

saver = FuncFormatter


def open_dir(path):
    """在资源管理器里打开这个目录"""
    if platform.system() == 'Windows':
        os.system('explorer.exe ' + path)
    if platform.system() == 'Darwin':
        os.system('open ' + path)
    elif platform.system() == 'Linux':
        os.system('nemo ' + path)
    else:
        print("system not support.")
    return


def open_file(file):
    """打开文件"""
    os.system('code ' + file)


def get_line_x(**kwargs):
    left_margin = kwargs['left_margin']
    point_count = kwargs['point_count']
    interval = kwargs['interval']
    line_x = [left_margin]
    for i in range(1, point_count):
        line_x.append(line_x[-1] + interval)
    return line_x


def get_line_x_lim(**kwargs):
    left_margin = kwargs['left_margin']
    point_count = kwargs['point_count']
    interval = kwargs['interval']
    right_margin = kwargs['left_margin']
    return [0, left_margin + interval * (point_count - 1) + right_margin]


def get_bar_x(**kwargs):
    left_margin = kwargs['bar_left_margin']
    bar_width = kwargs['bar_width']
    bar_count = kwargs['bar_count']
    interval = kwargs['bar_interval']
    bar_x = [left_margin + bar_width / 2]
    for i in range(1, bar_count):
        bar_x.append(bar_x[-1] + bar_width + interval)
    return bar_x


def get_group_bar_x(**kwargs):
    left_margin = kwargs['left_margin']
    group_margin = kwargs['group_margin']
    bar_interval = kwargs['bar_interval']
    bar_width = kwargs['bar_width']
    bar_count_in_group = kwargs['bar_count_in_group']
    group_count = kwargs['group_count']

    bar_x = [left_margin + bar_width / 2]
    for i in range(1, group_count):
        for j in range(1, bar_count_in_group):
            bar_x.append(bar_x[-1] + bar_width + bar_interval)
        bar_x.append(bar_x[-1] + bar_width + group_margin)
    for i in range(1, bar_count_in_group):
        bar_x.append(bar_x[-1] + bar_width + bar_interval)
    return bar_x


def get_group_x(**kwargs):
    left_margin = kwargs['left_margin']
    group_margin = kwargs['group_margin']
    bar_interval = kwargs['bar_interval']
    bar_width = kwargs['bar_width']
    bar_count_in_group = kwargs['bar_count_in_group']
    group_count = kwargs['group_count']

    group_width = bar_width * bar_count_in_group + \
        bar_interval * (bar_count_in_group - 1)

    group_tick_x = [left_margin + 0.5 * group_width]
    for i in range(1, group_count):
        group_tick_x.append(group_tick_x[-1] + group_width + group_margin)
    return group_tick_x


def get_group_bar_x_lim(**kwargs):
    left_margin = kwargs['left_margin']
    right_margin = kwargs['right_margin']
    margin = kwargs['group_margin']
    interval = kwargs['bar_interval']
    bar_width = kwargs['bar_width']
    bar_count_in_group = kwargs['bar_count_in_group']
    group_count = kwargs['group_count']
    group_width = bar_width * bar_count_in_group + \
        interval * (bar_count_in_group - 1)

    return [0, left_margin + group_width * group_count + margin * (group_count - 1) + right_margin]


def get_bar_x_lim(**kwargs):
    bar_left_margin = kwargs['bar_left_margin']
    bar_count = kwargs['bar_count']
    bar_width = kwargs['bar_width']
    interval = kwargs['bar_interval']
    bar_right_margin = kwargs['bar_right_margin']
    return [0, bar_left_margin + (bar_width + interval) * (bar_count - 1) + bar_width + bar_right_margin]


def get_average(values):
    return sum(values) / len(values)


def get_mean(values):
    return get_average(values)


def load_values_vertical(file):
    f = open(file, 'r')
    values = []
    while True:
        line = f.readline()
        if line == '':
            break
        values.append(float(line.strip()))
    return values


def load_integers_vertical(file):
    f = open(file, 'r')
    values = []
    while True:
        line = f.readline()
        if line == '':
            break
        values.append(int(line.strip()))
    return values


def load_values(file):
    f = open(file, 'r')
    values = []
    while True:
        line = f.readline()
        if line == '':
            break
        for s in line.split():
            values.append(float(s.strip()))
    return values


def load_pair_values_vertical(file):
    f = open(file, 'r')
    values = []
    while True:
        line = f.readline()
        if line == '':
            break
        # print(line)
        value = []
        for raw in line.strip().split():
            value.append(float(raw))
        # values.append(float(line.strip()))
        values.append(value)
    return values


def K_formatter_speed_with_unit_and_Bps(value, pos):
    if value == 0:
        return '0'
    unit = ''
    if value >= 1024:
        unit = 'K'
        value /= 1024
        if value >= 1024:
            unit = 'M'
            value /= 1024
            if value >= 1024:
                unit = 'G'
                value /= 1024
    if int(value * 10) == int(value) * 10:
        return '%d' % int(value) + unit + 'Bps'
    else:
        return '%.1f' % value + unit + 'Bps'


def K_formatter_speed_with_unit_without_Bps(value, pos):
    if value == 0:
        return '0'
    unit = ''
    if value >= 1024:
        unit = 'K'
        value /= 1024
        if value >= 1024:
            unit = 'M'
            value /= 1024
            if value >= 1024:
                unit = 'G'
                value /= 1024

    if value - int(value) == 0:
        return '%d' % int(value) + unit
    else:
        value = int(value * 10) / 10
        if value - int(value) == 0:
            return '%d' % int(value) + unit
        if value < 1:
            return '%.1f' % float(value) + unit
        else:
            return '%d' % int(value) + unit

    # if int(value*10) == int(value)*10:
    #     return '%d' % int(value) + unit
    # else:
    #     return '%.1f' % value + unit


def time_format_from_sec(value, pos):
    if value == 0:
        return '0'

    unit = ''
    if value >= 1:
        unit = 's'
    else:
        value *= 1000
        unit = 'ms'

    if value - int(value) == 0:
        return '%d' % int(value) + unit
    else:
        value = int(value * 10) / 10
        if value - int(value) == 0:
            return '%d' % int(value) + unit
        return '%.1f' % float(value) + unit


def time_format_from_sec_without_unit(value, pos):
    if value == 0:
        return '0'

    unit = ''
    if value >= 1:
        unit = 's'
    # else:
    #     value *= 1000
    #     unit = 'ms'

    if value - int(value) == 0:
        return '%d' % int(value)
    else:
        value = int(value * 10) / 10
        if value - int(value) == 0:
            return '%d' % int(value)
        return '%.1f' % float(value)


def K_formatter_integer_size(value, pos):
    if value == 0:
        return '0'
    unit = ''
    if value >= 1024:
        unit = 'K'
        value /= 1024
        if value >= 1024:
            unit = 'M'
            value /= 1024
            if value >= 1024:
                unit = 'G'
                value /= 1024
    if value - int(value) == 0:
        return '%d' % int(value) + unit + 'B'
    else:
        value = int(value * 10) / 10
        if value - int(value) == 0:
            return '%d' % int(value) + unit + 'B'
        if value < 1:
            return '%.1f' % float(value) + unit + 'B'
        else:
            return '%d' % int(value) + unit + 'B'


def K_formatter_without_unit(value, pos):
    if value == 0:
        return '0'
    unit = ''
    if value >= 1024:
        unit = 'K'
        value /= 1024
        if value >= 1024:
            unit = 'M'
            value /= 1024
            if value >= 1024:
                unit = 'G'
                value /= 1024
    if value == int(value) and value >= 10:
        return '%d' % int(value)
    return '%.1f' % value


def k_formatter_without_unit(value, pos):
    if value == 0:
        return '0'
    unit = ''
    if value >= 1000:
        unit = 'K'
        value /= 1000
        if value >= 1000:
            unit = 'M'
            value /= 1000
            if value >= 1000:
                unit = 'G'
                value /= 1000
    if value == int(value) and value >= 10:
        return '%d' % int(value)
    return '%.1f' % value


def get_axis(**kwargs):
    # matplotlib = kwargs['matplotlib']
    tick_length = kwargs['tick_length']
    line_width = kwargs['line_width']
    figure_width = kwargs['figure_width']
    figure_height = kwargs['figure_height']
    col = kwargs['col']
    row = kwargs['row']
    xtick_pad = kwargs['xtick_pad']
    ytick_pad = kwargs['ytick_pad']
    font_size = kwargs['font_size']
    font_family = kwargs['font_family']

    matplotlib.rcParams['xtick.major.size'] = tick_length
    matplotlib.rcParams['xtick.major.width'] = line_width
    matplotlib.rcParams['ytick.major.size'] = tick_length
    matplotlib.rcParams['ytick.major.width'] = line_width
    matplotlib.rcParams['xtick.major.pad'] = str(xtick_pad)
    matplotlib.rcParams['ytick.major.pad'] = str(ytick_pad)

    matplotlib.rcParams['figure.dpi'] = 1800
    matplotlib.rcParams['savefig.dpi'] = 1800
    matplotlib.rcParams['hatch.linewidth'] = line_width
    matplotlib.rcParams['lines.linewidth'] = line_width 

    fig = matplotlib.pyplot.figure(figsize=(figure_width, figure_height))

    height_ratios = []
    width_ratios = []
    for i in range(0, col):
        width_ratios.append(1)
    for i in range(0, row):
        height_ratios.append(1)

    if 'height_ratios' in kwargs:
        height_ratios = kwargs['height_ratios']
    if 'width_ratios' in kwargs:
        width_ratios = kwargs['width_ratios']

    gs = matplotlib.gridspec.GridSpec(
        row, col, height_ratios=height_ratios, width_ratios=width_ratios)

    ax = []
    for i in range(0, row * col):
        ax.append(matplotlib.pyplot.subplot(gs[i]))

        # if 'font_size' in kwargs:
    for _ax in ax:
        for tick in _ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(font_size)
        for tick in _ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(font_size)

    for _ax in ax:
        for tick in _ax.yaxis.get_major_ticks():
            tick.label1.set_family(font_family)
        for tick in _ax.xaxis.get_major_ticks():
            tick.label1.set_family(font_family)

    for _ax in ax:
        for tick in _ax.yaxis.get_major_ticks():
            tick.label2.set_fontsize(font_size)
        for tick in _ax.xaxis.get_major_ticks():
            tick.label2.set_fontsize(font_size)

    for _ax in ax:
        for tick in _ax.yaxis.get_major_ticks():
            tick.label2.set_family(font_family)
        for tick in _ax.xaxis.get_major_ticks():
            tick.label2.set_family(font_family)
    
    for _ax in ax:
        _ax.spines['top'].set_linewidth(1)    # 设置上边框的粗细
        _ax.spines['bottom'].set_linewidth(1) # 设置下边框的粗细
        _ax.spines['left'].set_linewidth(1)   # 设置左边框的粗细
        _ax.spines['right'].set_linewidth(1)  # 设置右边框的粗细
    return ax


def delete_file(file_name):
    if os.name == 'nt':
        os.system('del /q /f ' + file_name)
    elif os.name == 'posix':
        os.system('rm -f ' + file_name)
    else:
        print("system not support.")
    return


def save_fig(**kwargs):
    file_name = kwargs['file_name']
    # matplotlib = kwargs['matplotlib']
    h_pad = kwargs['h_pad']
    w_pad = kwargs['w_pad']
    # is_open_dir = kwargs['open_dir']
    is_open_file = kwargs['open_file']
    line_width = kwargs['line_width']

    matplotlib.rcParams['figure.dpi'] = 1800
    matplotlib.rcParams['savefig.dpi'] = 1800
    matplotlib.rcParams['hatch.linewidth'] = line_width
    matplotlib.rcParams['lines.linewidth'] = line_width
    matplotlib.rcParams['pdf.fonttype'] = 42  # 在IEEE网站提交需要嵌入字体
    matplotlib.rcParams['ps.fonttype'] = 42  # 在IEEE网站提交需要嵌入字体

    matplotlib.pyplot.tight_layout(h_pad=h_pad, w_pad=w_pad)
    # output_dir = pathlib.Path(__file__).parent
    # print(__file__)
    # output_dir = os.path.join(pathlib.Path(__file__).parent, 'pics')
    # output_dir = '.' + os.sep + 'pics' + os.sep
    output_file = file_name
    # output_file = os.path.join(output_dir, file_name)
    delete_file(output_file)
    print(output_file)

    matplotlib.pyplot.savefig(
        output_file, transparent=True, bbox_inches='tight', pad_inches=0.01, dpi=1800)
    # if is_open_dir:
    #     open_dir(output_dir)
    if is_open_file:
        open_file(output_file)
    if 'copy_to' in kwargs:
        for target in kwargs['copy_to']:
            copyfile(output_file, os.path.join(target,file_name))


def generate_random_data_list(standard, group_number=20, variation=0.2):
    data_list = []
    for i in range(0, group_number):
        data_list.append(standard + (random.randint(0, 65536) %
                         2 - 0.5) * 2 * standard * variation * random.random())
    return data_list


def generate_random_value(random, standard, variation=0.2):
    return standard + (random.randint(0, 65536) % 2 - 0.5) * 2 * standard * variation * random.random()


def create_file(file_name):
    if os.path.exists(file_name):
        return
    file = open(file_name, 'w+')
    file.close()


def get_bar_error(values):
    average = get_average(values)
    max_diff = 0
    for value in values:
        max_diff = max(max_diff, abs(value - average))
    return max_diff


def list_divid_value(l, v):
    new_l = []
    for lv in l:
        new_l.append(lv / v)
    return new_l


def draw_cdf(ax, data, **kwargs):
    if 'bins' in kwargs:
        bins = kwargs['bins']
    else:
        bins = 1000000
    values, base = numpy.histogram(data, bins=bins)
    cumulative = numpy.cumsum(values)
    lines = ax.plot(
        base[:-1],
        list_divid_value(cumulative, len(data)),
        color=kwargs['color'],
        linewidth=kwargs['linewidth'],
        linestyle=kwargs['linestyle'],
        label=kwargs['label']
    )
    return lines


def format_to_integer(value, pos):
    return '%d' % int(value)


def percentage_formatter(value, pos):
    return '%d' % int(value * 100)


def get_absolute_on_log(relative, y_lim):
    y_min = y_lim[0]
    y_max = y_lim[1]
    return y_max ** relative / y_min ** (relative - 1)


def get_relative_on_log(absolute, y_lim):
    y_min = y_lim[0]
    y_max = y_lim[1]
    return math.log(absolute / y_max) / math.log(y_max / y_min) + 1


def get_absolute_on_linear(relative, y_lim):
    return relative * (y_lim[1] - y_lim[0]) + y_lim[0]


def get_relative_on_linear(absolute, y_lim):
    return (absolute - y_lim[0]) / (y_lim[1] - y_lim[0])


def list_add(lists):
    l = lists[0]
    for i in range(1, len(lists)):
        for j in range(len(l)):
            l[j] += lists[i][j]
    return l


def vector_add(lists):
    return list_add(lists)


def get_mean_vector(ll):
    means = []
    for l in ll:
        sum = 0
        for v in l:
            sum += v
        means.append(sum / len(l) / 1000)
    return means


def draw_legend(ax, **kwargs):
    plots = kwargs['plots']
    labels = kwargs['labels']
    location = kwargs['location']
    ncol = kwargs['ncol']
    font_size = kwargs['font_size']
    font_family = kwargs['font_family']
    handletextpad = kwargs['handletextpad']
    columnspacing = kwargs['columnspacing']
    ax.legend(
        plots,
        labels,
        loc=location,
        ncol=ncol,
        numpoints=1,
        prop={
            'family': font_family,
            'size': font_size
        },
        framealpha=1,
        handletextpad=handletextpad,
        columnspacing=columnspacing,
    ).get_frame().set_linewidth(0.1)


def generate_ticks(num, bound, log=False):
    ticks = [bound[0]]
    if not log:
        dis = (bound[1] - bound[0]) / (num + 1)
        for i in range(0, num):
            ticks.append(ticks[-1] + dis)
    else:
        times = (bound[1] / bound[0]) ** (1 / (num + 1))
        for i in range(0, num):
            ticks.append(ticks[-1] * times)
    ticks.append(bound[1])
    return ticks
