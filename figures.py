"""一些简单的绘图函数，调用即绘图"""
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import futils.paper_figures.measure as measure
import futils.paper_figures.tools as tools


def draw_plot(x, y, output_name='matplotlib.png'):
    """绘制折线图"""
    plt.figure()
    plt.plot(x, y)
    plt.savefig(output_name)
    plt.show()


def draw_plot_multi_y(data, output_name='matplotlib.png', legend_label=None,
                      xlabel=None, ylabel=None):
    """绘制带有多个曲线的条形图，并配有图例
    输入数据中data是一个包含多个由[x,y]组成的list：
        data = [[x1,y1], [x2,y2], [x3,y3], ...]
    其中xi,yi是一个曲线中各点横坐标的list、纵坐标的list
    """
    plt.figure()
    rts = []  # return values
    data = list(data)
    for item in data:
        x, = plt.plot(item[0], item[1])
        rts.append(x)
    # draw legend
    if legend_label is None:
        legend_label = []
        for i in range(len(data)):
            legend_label.append('Line'+str(i+1))
    plt.legend(rts, legend_label, loc=0)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    # save pic
    plt.savefig(output_name)
    plt.show()


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
    # 载入参数
    line_width = measure.line_width_normal
    font_size = 11
    font_family = "Arial"
    
    figure_width = 4.2
    if 'figure_width' in kwargs:
        figure_width = kwargs['figure_width']
    
    figure_height = 2.6
    if 'figure_height' in kwargs:
        figure_height = kwargs['figure_height']
    
    assert len(data)>=1
    ax = tools.get_axis(
        tick_length=2.0,
        line_width=line_width,
        figure_width=figure_width,
        figure_height=figure_height,
        col=1, row=1,
        xtick_pad=measure.xtick_pad_normal,
        ytick_pad=measure.ytick_pad_normal,
        font_size=font_size,
        font_family=font_family
    )
    
    # 单一CDF图，不再绘制legend
    
    plot = []
    for item in data:
        ecdf = sm.distributions.ECDF(item)
        x = np.linspace(min(item), max(item), 1000)
        y = ecdf(x)
        _p, = ax[0].step(x, y, mfc='none', ms=4, linewidth=2.0)
        plot.append(_p)

    
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
    
    if 'xlabel' in kwargs:
        ax[0].set_xlabel(kwargs['xlabel'], fontfamily=font_family, fontsize = font_size)
    if 'ylabel' in kwargs:
        ax[0].set_ylabel(kwargs['ylabel'], fontfamily=font_family, fontsize = font_size)
    
    
    have_legend = True
    if len(data) >= 2 and 'legend_labels' not in kwargs:
        legend_labels = []
        for i in range(len(data)):
            legend_labels.append('Line'+str(i+1))
    elif len(data) == 1 and 'legend_labels' not in kwargs:
        have_legend = False
    else:
        legend_labels = kwargs['legend_labels']
        
        
    if have_legend:
        print(legend_labels)
        tools.draw_legend(
            ax[0],
            plots=plot,
            labels=legend_labels,
            location=0,
            ncol=1,
            font_size=font_size * 0.75,
            font_family=font_family
        )
    
    if 'output_name' in kwargs:
        plt.savefig(kwargs['output_name'])
    else:
        plt.savefig('matplotlib.png')
    
    

def draw_cdf(data, **kwargs):
    """给一个数组，绘制这个数组的CDF图
    可选参数：
    output_name='matplotlib.png',
    无默认参数的参数：
    xticks, yticks, xlim, ylim, xlabel, ylabel
    """
    return draw_cdf_multi_y([data], **kwargs)


def draw_hist(data ,output_name='matplotlib.png'):
    plt.hist(data, bins='auto', alpha=0.7, rwidth=0.85, color='blue', edgecolor='black')
    plt.grid(axis='y', alpha=0.75)  # 添加网格线    
    plt.savefig(output_name)
    plt.show()
    plt.show()  # 显示直方图


