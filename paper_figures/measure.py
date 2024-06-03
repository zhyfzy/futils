#!/usr/bin/env python3

# suggested figure width
figure_width_wide = 5

figure_width_half = 3.67
figure_width_single = 3.2
figure_width_one_and_half = 5
figure_width_double = 6
figure_width_quad = 13

# suggested figure height
figure_height_small = 1.8
figure_height_normal = 2.2

figure_height_half = 1.6
figure_height_single = 2
figure_height_double = 4.4

# suggested font
font_size_normal = 9
font_size_small = 8
font_size_large = 12
font_size_huge = 14
helvetica = 'Helvetica'
arial = 'Arial'
times_new_roman = 'Times New Roman'
calibre = 'Calibre'
bitstream = 'Bitstream Vera Sans'
font_family_normal = times_new_roman

# suggested line width
line_width_normal = 0.2
line_width_bold = 1.6
line_width_light = 0.6

# tick
tick_length_normal = 0.2
tick_pad_normal = 5

xtick_pad_normal = 5
ytick_pad_normal = 5

h_pad_normal = 1
w_pad_normal = 1
h_pad_single = 0.01
w_pad_single = 0.01


bar_width = 1.25 + 0.25
bar_interval = 0.5

group_left_margin = 2
group_right_margin = 2
group_margin = 2 + 0.25

# colors
red = 'r'
blue = 'blue'
black = 'k'
white = 'w'
yellow = 'y'
green = 'g'

pink = (255 / 255, 192 / 255, 203 / 255)

yellow_chrome = (255 / 255, 206 / 255, 68 / 255)
green_chrome = (28 / 255, 162 / 255, 97 / 255)
red_chrome = (222 / 255, 83 / 255, 71 / 255)
blue_chrome = (75 / 255, 139 / 255, 245 / 255)

grey_light = (223 / 255, 223 / 255, 223 / 255)
grey_heavy = (82 / 255, 82 / 255, 82 / 255)
grey_middle = (
    (grey_heavy[0] + grey_light[0]) / 2,
    (grey_heavy[0] + grey_light[0]) / 2,
    (grey_heavy[0] + grey_light[0]) / 2,
)
orange = (
    255 / 255, 165 / 255, 0
)
purple = (
    128 / 255, 0 / 255, 128 / 255
)

def gray_color(degree: int):
    return (degree / 255, degree / 255, degree / 255)

# unit
K = 1024
M = K * 1024
G = M * 1024

k = 1000
m = k * 1000
g = m * 1000