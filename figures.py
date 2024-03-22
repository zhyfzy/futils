"""一些简单的绘图函数，调用即绘图"""
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np
import statsmodels.api as sm
import futils.paper_figures.measure as measure
import futils.paper_figures.tools as tools

def __style_a(data, data_parse_func, **kwargs):
    # 载入参数
    frame_linewidth = kwargs.get('frame_linewidth', measure.line_width_normal)
    font_size = 11
    font_family = kwargs.get('font_family', 'sans-serif')
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
        print(legend_labels)
        tools.draw_legend(
            ax[0],
            plots=plot,
            labels=legend_labels,
            location=legend_location,
            ncol=legend_ncol,
            font_size=font_size * 0.75,
            font_family=font_family
        )

    output_name = kwargs.get('output_name', 'matplotlib.png')
    tools.save_fig(
        file_name=output_name,
        line_width=frame_linewidth,
        h_pad=measure.h_pad_single,
        w_pad=measure.w_pad_single,
        open_file=True
    )


def draw_scatter_multi_y(data, output_name='matplotlib.png',
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
    output_name='matplotlib.png',
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
    """绘制带有多个曲线的条形图，并配有图例
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


def draw_hist(data, output_name='matplotlib.png'):
    plt.hist(data, bins='auto', alpha=0.7, rwidth=0.85,
             color='blue', edgecolor='black')
    plt.grid(axis='y', alpha=0.75)  # 添加网格线
    plt.savefig(output_name)
    plt.show()
    plt.show()  # 显示直方图
