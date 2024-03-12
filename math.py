"""常用的一些数学函数"""
from typing import List
EPS = 0.000001  # 用于浮点数比较


def flat_list(_list):
    """将一个list中的数相乘"""
    result = 1
    for i in _list:
        result *= i
    return result


def float_equal(a, b):
    """判断浮点数是否相等"""
    return abs(a-b) < EPS


def float_less_equal(a, b):
    """判断浮点数a是否小于等于b"""
    if a < b:
        return True
    if float_equal(a, b):
        return True
    return False


def float_great_equal(a, b):
    """判断浮点数a是否大于b"""
    if a > b:
        return True
    if float_equal(a, b):
        return True
    return False


def float_to_int(a):
    """将浮点数转换为int"""
    if a > 0:
        return int(a+EPS)
    return int(a-EPS)


def div_up(a: int, b: int):
    """向上取整，要求a和b都是整数"""
    return (a + b - 1) // b


def div_down(a: int, b: int):
    """向下取整，要求a和b都是整数"""
    return a // b


def ceil(a: int, b: int):
    """向上近似：找到最小的值，满足大于等于a、且为b的整数倍。
    要求a和b都是整数"""
    return ((a - 1) // b + 1) * b


def floor(a: int, b: int):
    """向下近似，找到最大的值，满足小于等于a、且为b的整数倍。
    要求输入的a和b都是整数"""
    return a - a % b


def find_power_of_two_leq(value):  # leq: less or equal
    """找到刚好小于等于value的2的幂次数"""
    power = 0
    while 2**power <= value:
        power += 1
    return 2**(power - 1)


def find_power_of_two_req(value):  # req: large or equal
    """找到刚好大于等于value的2的幂次数"""
    power = 0
    while 2**power < value:
        power += 1
    return 2**power


def find_power_of_two_less(value):
    """找到刚好小于value的2的幂次数"""
    power = 0
    while 2**power < value:
        power += 1
    return 2**(power - 1)


def find_power_of_two_large(value):
    """找到刚好大于value的2的幂次数"""
    power = 0
    while 2**power <= value:
        power += 1
    return 2**power


def dim1_to_dim2(dim1_id: int, dim2_w: int, dim1_first_id=0, dim2_first_id=0):
    """一维id转二维id
    如二维是 4x5 的矩阵 (dim2_w = 5, 每行5个元素)
     0  1  2  3  4
     5  6  7  8  9
    10 11 12 13 14
    15 16 17 18 19
    比如输入11，返回的就是二维的坐标[2,1]
    dim1_first_id=1 即首个id是1
    dim2_first_id=1 表示第一行或列的id是1（默认是从0开始计算的）"""
    return ((dim1_id-dim1_first_id) // dim2_w + dim2_first_id,
            (dim1_id-dim1_first_id) % dim2_w + dim2_first_id)


def dim2_to_dim1(dim2_id: List[int], dim2_w: int, dim1_first_id=0,
                 dim2_first_id=0):
    """二维id转一维id
    如二维是 4x5 的矩阵 (dim2_w = 5, 每行5个元素)
     0  1  2  3  4
     5  6  7  8  9
    10 11 12 13 14
    15 16 17 18 19
    比如输入[2,1]，返回的就是一维的坐标11
    dim1_first_id=1 即首个id是1
    dim2_first_id=1 表示第一行或列的id是1（默认是从0开始计算的）"""
    _a = (dim2_id[0]-dim2_first_id) * dim2_w
    _b = (dim2_id[1] - dim2_first_id) + dim1_first_id
    return _a + _b


def min_with_exception(num_list, execption=-1):
    """给定一个list数组，求这些数中的最小值。
    其中数组中的数可能有例外值，如-1或None等，需要排除掉这些例外值"""
    ret = execption
    for n in num_list:
        if n != execption:
            if ret == execption:
                ret = n
            else:
                ret = min(ret, n)
    return ret
