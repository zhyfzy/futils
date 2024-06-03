"""一些简单的绘图函数，调用即绘图"""
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np
import statsmodels.api as sm
import futils.paper_figures.measure as measure
import futils.paper_figures.tools as tools


def __style_a(data, data_parse_func, **kwargs):
    """参数：
    【预处理阶段】
    frame_linewidth: 边框的宽度，默认measure.line_width_normal=0.2
    font_family: 默认宋体
    font_size: 默认11号字体
    figure_width: 图片的宽度
    figure_height: 图片的高度
    xtick_pad: 坐标轴刻度线长度
    ytick_pad: 坐标轴刻度线长度

    【绘图的回调函数(仅限plot/step/cdf)】
    curve_linewidth: 图中曲线的宽度
    color: 一个list表示各个曲线的颜色
    marker: 在曲线中，每个数据点处的标识，可以是圆圈、三角等符号。
    ms: marker的大小

    【绘图的回调函数(仅限bar)】
    group_name: 在横坐标展示的group的名称
    bar_yerr: error bar的数据

    【后处理】
    xticks: x坐标轴有哪些刻度
    yticks: y坐标轴有哪些刻度
    xlim: x坐标轴的范围
    ylim: y坐标轴的范围
    title: 图表标题
    xlabel: x坐标轴
    ylabel: y坐标轴
    legend_labels: 图例中的文字，是个list
    legend_ncol: 图例的列数
    legend_location: 图例的位置
    output_name: 图片保存到哪里
    """
    frame_linewidth = kwargs.get('frame_linewidth', measure.line_width_normal)
    kwargs['frame_linewidth'] = frame_linewidth
    font_size = kwargs.get('font_size', 11)
    kwargs['font_size'] = 11
    font_family = kwargs.get('font_family', 'sans-serif')
    kwargs['font_family'] = font_family
    if font_family == 'sans-serif':
        matplotlib.rcParams['font.sans-serif'] = ['SimSun']

    figure_width = kwargs.get('figure_width', 4.2)
    figure_height = kwargs.get('figure_height', 2.6)

    xtick_pad = kwargs.get('xtick_pad', measure.xtick_pad_normal)
    ytick_pad = kwargs.get('ytick_pad', measure.xtick_pad_normal)

    assert len(data) >= 1
    ax = tools.get_axis(
        tick_length=2.0,
        line_width=frame_linewidth,
        figure_width=figure_width,
        figure_height=figure_height,
        col=1, row=1,
        xtick_pad=xtick_pad,
        ytick_pad=ytick_pad,
        font_size=font_size,
        font_family=font_family
    )

    # parse linewidth
    curve_linewidth = kwargs.get('curve_linewidth', 1.0)
    if isinstance(curve_linewidth, list):
        assert len(curve_linewidth) == len(data)
    else:
        curve_linewidth = [curve_linewidth] * len(data)
    kwargs['curve_linewidth'] = curve_linewidth

    # parse color
    color = kwargs.get('color', [measure.purple, measure.green_chrome,
                                 measure.blue_chrome, measure.orange,
                                 measure.yellow, measure.red_chrome,
                                 measure.yellow_chrome, measure.grey_heavy])
    assert isinstance(color, list)
    color = color[:len(data)]
    for i, _color in enumerate(color):
        # 转换格式，如果是int的rgb值，转换为浮点数的格式
        if isinstance(_color[0], int):
            color[i] = (_color[0]/255, _color[1]/255, _color[2]/255)
    kwargs['color'] = color

    # parse marker
    # https://matplotlib.org/stable/gallery/lines_bars_and_markers/marker_reference.html
    marker = kwargs.get('marker', ['.', 'D', '^', 'o', 's', '*', 'v', 'p'])
    assert isinstance(marker, list)
    marker = marker[:len(data)]
    kwargs['marker'] = marker

    # parse marker size
    ms = kwargs.get('ms', 4)
    if isinstance(ms, list):
        assert len(ms) == len(data)
    else:
        ms = [ms] * len(data)
    kwargs['ms'] = ms

    plot = data_parse_func(data, ax, **kwargs)

    ax[0].xaxis.grid(linestyle=':', zorder=-1,
                     color=(151 / 255, 151 / 255, 151 / 255))
    ax[0].yaxis.grid(linestyle=':', zorder=-1,
                     color=(151 / 255, 151 / 255, 151 / 255))

    for tick in ax[0].yaxis.get_major_ticks():
        tick.label1.set_fontsize(font_size)
        tick.label1.set_family(font_family)
    for tick in ax[0].xaxis.get_major_ticks():
        tick.label1.set_fontsize(font_size)
        tick.label1.set_family(font_family)

    if 'xticks' in kwargs:
        ax[0].set_xticks(kwargs['xticks'])
    if 'xlim' in kwargs:
        ax[0].set_xlim(kwargs['xlim'])
    if 'yticks' in kwargs:
        ax[0].set_yticks(kwargs['yticks'])
    if 'ylim' in kwargs:
        ax[0].set_ylim(kwargs['ylim'])
    if 'title' in kwargs:
        ax[0].set_title(kwargs['title'])

    if 'xlabel' in kwargs:
        ax[0].set_xlabel(kwargs['xlabel'],
                         fontfamily=font_family, fontsize=font_size)
    if 'ylabel' in kwargs:
        ax[0].set_ylabel(kwargs['ylabel'],
                         fontfamily=font_family, fontsize=font_size)

    if 'figure_type' in kwargs and kwargs['figure_type'] == 'bar':
        # 设置legend_labels:
        have_legend = True
        legend_labels = kwargs.get('legend_labels', None)
        if legend_labels is None:
            legend_labels = []
            for i in range(len(data[0])):
                legend_labels.append(f'Item{i}')
    else:
        have_legend = True
        if len(data) >= 2 and 'legend_labels' not in kwargs:
            legend_labels = []
            for i in range(len(data)):
                legend_labels.append('Line'+str(i+1))
        elif len(data) == 1 and 'legend_labels' not in kwargs:
            have_legend = False
        else:
            legend_labels = kwargs['legend_labels']

    legend_ncol = kwargs.get('legend_ncol', 1)
    legend_location = kwargs.get('legend_location', 0)

    if have_legend:
        tools.draw_legend(
            ax[0],
            plots=plot,
            labels=legend_labels,
            location=legend_location,
            ncol=legend_ncol,
            font_size=font_size * 0.75,
            font_family=font_family
        )

    output_name = kwargs.get('output_name', 'matplotlib.pdf')
    tools.save_fig(
        file_name=output_name,
        line_width=frame_linewidth,
        h_pad=measure.h_pad_single,
        w_pad=measure.w_pad_single,
        open_file=True
    )


def draw_scatter_multi_y(data, output_name='matplotlib.pdf',
                         legend_label=None):
    """绘制带有多组数据的散点图，并配有图例"""
    plt.figure()
    rts = []  # return values
    for item in data:
        x = plt.scatter(item[0], item[1], s=0.1)
        rts.append(x)
    # draw legend
    if legend_label is None:
        legend_label = []
        for i in range(len(data)):
            legend_label.append('Line'+str(i+1))
    plt.legend(rts, legend_label, loc=0)
    # save pic
    plt.savefig(output_name)
    plt.show()


def draw_cdf_multi_y(data, **kwargs):
    """为多组数据绘制CDF图，并配有图例"""
    def data_parse_callback(data, ax, **kwargs):
        plot = []
        for item in data:
            ecdf = sm.distributions.ECDF(item)
            x = np.linspace(min(item), max(item), 1000)
            y = ecdf(x)
            _p, = ax[0].step(x, y, mfc='none', ms=4, linewidth=2.0)
            plot.append(_p)
        return plot
    return __style_a(data, data_parse_callback, **kwargs)


def draw_cdf(data, **kwargs):
    """给一个数组，绘制这个数组的CDF图
    可选参数：
    output_name='matplotlib.pdf',
    无默认参数的参数：
    xticks, yticks, xlim, ylim, xlabel, ylabel
    """
    return draw_cdf_multi_y([data], **kwargs)


def draw_step(x, y, **kwargs):
    return draw_step_multi_y([[x, y]], **kwargs)


def draw_step_multi_y(data, **kwargs):
    """绘制带有多个曲线的step图，并配有图例
    输入数据中data是一个包含多个由[x,y]组成的list：
        data = [[x1,y1], [x2,y2], [x3,y3], ...]
    其中xi,yi是一个曲线中各点横坐标的list、纵坐标的list
    """
    def data_parse_callback(data, ax, **kwargs):
        plot = []
        where = kwargs.get('where', 'pre')
        linewidth = kwargs['curve_linewidth']
        marker = kwargs['marker']
        color = kwargs['color']
        ms = kwargs['ms']

        for item, _linewidth, _marker, _color, _ms in zip(data, linewidth, marker, color, ms):
            x = item[0]
            y = item[1]
            _p, = ax[0].step(x, y, ms=_ms, linewidth=_linewidth,
                             where=where, marker=_marker, color=_color)
            plot.append(_p)
        return plot
    return __style_a(data, data_parse_callback, **kwargs)


def draw_plot(x, y, **kwargs):
    """绘制折线图"""
    return draw_plot_multi_y([[x, y]], **kwargs)


def draw_plot_multi_y(data, **kwargs):
    """绘制带有多个曲线的折线图，并配有图例
    输入数据中data是一个包含多个由[x,y]组成的list：
        data = [[x1,y1], [x2,y2], [x3,y3], ...]
    其中xi,yi是一个曲线中各点横坐标的list、纵坐标的list
    """
    def data_parse_callback(data, ax, **kwargs):
        plot = []
        linewidth = kwargs['curve_linewidth']
        marker = kwargs['marker']
        color = kwargs['color']
        ms = kwargs['ms']

        for item, _linewidth, _marker, _color, _ms in zip(data, linewidth, marker, color, ms):
            x = item[0]
            y = item[1]
            _p, = ax[0].plot(x, y, ms=_ms, linewidth=_linewidth,
                             marker=_marker, color=_color)
            plot.append(_p)
        return plot
    return __style_a(data, data_parse_callback, **kwargs)


def draw_bar(data, **kwargs):
    """绘制带有多组数据的条形图，并配有图例
    首先，数据需要有多个group，每个group的数据在条形图中是连在一起的，使用【图例】区分group内的数据
    然后，不同group之间会存在间隔，用户需要提供group_name，表示不同group在x坐标轴上的名称

    data数据需要是这样的形式：
    [[1,2,3,4], [5,6,7,8]] 它是二位数组，第一维表示不同group，第二位表示group内的数据
    """
    kwargs['figure_type'] = 'bar'

    def data_parse_callback(data, ax, **kwargs):
        bar_count_in_group = len(data[0])
        group_count = len(data)
        bar_x = tools.get_group_bar_x(
            left_margin=measure.group_left_margin,
            group_margin=measure.group_margin,
            bar_width=measure.bar_width,
            bar_interval=measure.bar_interval,
            bar_count_in_group=bar_count_in_group,
            group_count=group_count,
        )
        if 'xlim' not in kwargs:
            bar_x_lim = tools.get_group_bar_x_lim(
                left_margin=measure.group_left_margin,
                group_margin=measure.group_margin,
                bar_width=measure.bar_width,
                bar_interval=measure.bar_interval,
                bar_count_in_group=bar_count_in_group,
                group_count=group_count,
                right_margin=measure.group_right_margin
            )
            ax[0].set_xlim(bar_x_lim)

        if 'xticks' not in kwargs:
            group_x = tools.get_group_x(
                left_margin=measure.group_left_margin,
                group_margin=measure.group_margin,
                bar_width=measure.bar_width,
                bar_interval=measure.bar_interval,
                bar_count_in_group=bar_count_in_group,
                group_count=group_count,
            )
            ax[0].set_xticks(group_x)

        ax[0].xaxis.grid(linestyle=':', zorder=-1,
                         color=(151 / 255, 151 / 255, 151 / 255))
        ax[0].yaxis.grid(linestyle=':', zorder=-1,
                         color=(151 / 255, 151 / 255, 151 / 255))
        error_params = dict(elinewidth=1.5,
                            ecolor=measure.red_chrome,
                            capsize=3.5)
        bar_data = []
        for item in data:
            bar_data.extend(item)

        bar_yerr = kwargs.get('bar_yerr', None)

        bars = ax[0].bar(bar_x, bar_data, width=measure.bar_width,
                         yerr=bar_yerr, error_kw=error_params, zorder=3)

        # 设置bar样式
        g75 = measure.gray_color(75)
        colors = [g75, g75, g75, g75, g75, g75]  # bar的边框颜色
        # 填充物 [None, 'xxxx', '\\\\\\\\', None, '////', 'xxxx']
        hatchs = [None, None, None, None, None, None]
        facecolors = [measure.red_chrome, measure.orange, measure.yellow,
                      measure.yellow_chrome, measure.green_chrome, measure.blue_chrome]  # 填充颜色
        while len(colors) < bar_count_in_group:
            colors.extend(colors)
            hatchs.extend(hatchs)
            facecolors.extend(facecolors)
        colors = colors[:bar_count_in_group] * group_count
        hatchs = hatchs[:bar_count_in_group] * group_count
        facecolors = facecolors[:bar_count_in_group] * group_count
        zips = zip(bars, colors, hatchs, facecolors)

        for _bar, color, hatch, facecolor in zips:
            _bar.set_color(color)
            _bar.set_facecolor(facecolor)
            _bar.set(hatch=hatch)
            _bar.set_linewidth(0.8)
            _bar.set_alpha(0.8)

        # 设置group_name
        group_name = kwargs.get('group_name', None)
        if group_name is None:
            group_name = []
            for i in range(group_count):
                group_name.append(f"Group{i}")

        ax[0].set_xticklabels(group_name,
                              fontsize=kwargs['font_size'],
                              family=kwargs['font_family'])
        ax[0].yaxis.set_major_formatter(tools.FuncFormatter(
            tools.time_format_from_sec_without_unit))

        return bars
    return __style_a(data, data_parse_callback, **kwargs)


def draw_hist(data, output_name='matplotlib.pdf'):
    plt.hist(data, bins='auto', alpha=0.7, rwidth=0.85,
             color='blue', edgecolor='black')
    plt.grid(axis='y', alpha=0.75)  # 添加网格线
    plt.savefig(output_name)
    plt.show()
    plt.show()  # 显示直方图
