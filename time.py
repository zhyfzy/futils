import datetime
from datetime import timezone
import time


def unix_time_to_str(st, _format="%Y-%m-%d %H:%M:%S", utc=False):
    """将unix时间（单位：秒），转换为字符串
    使用范例：print(unix_time_to_str(time.time()))
    """
    if utc:
        dt = datetime.datetime.utcfromtimestamp(st)
        return dt.strftime(_format)
    return time.strftime(_format, time.localtime(st))

def get_timestamp(_format="%Y-%m-%d %H:%M:%S", utc=False):
    st = time.time()
    return unix_time_to_str(st, _format, utc)

def unix_time_to_str_date(st, _format="%Y-%m-%d", utc=False):
    """将unix时间（单位：秒），转换为字符串
    使用范例：print(unix_time_to_str(time.time()))
    """
    return unix_time_to_str(st, _format, utc)


def str_to_unix_time(st, _format="%Y-%m-%d %H:%M:%S", utc=False):
    """将日期+时间（如2024-03-07 12:00:00）转化为unix时间（单位：秒）
    utc=False的时候按照当前时区计算，否则按照utc时间计算"""
    if utc:
        dt = datetime.datetime.strptime(st, _format)
        unix_timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
        return unix_timestamp
    return datetime.datetime.strptime(st, _format).timestamp()


def str_date_to_unix_time(st, _format="%Y-%m-%d", utc=False):
    """将日期（如2024-03-07）转化为unix时间（单位：秒）
    utc=False的时候按照当前时区计算，否则按照utc时间计算"""
    return str_to_unix_time(st, _format, utc)


def unix_time_add_day(st, day_count):
    """某个unix时间（单位：秒）在st天后的unix时间
    st可以是负数"""
    st = st + day_count * 86400
    return st
    

# # 日期时间字符串
# st = "2017-11-23 16:10:10" # 当前日期时间
# dt = datetime.datetime.now()
# # 当前时间戳
# sp = time.time()

# # 1.把datetime转成字符串
# def datetime_toString(dt):
#     print("1.把datetime转成字符串: ", dt.strftime("%Y-%m-%d %H:%M:%S"))

# # 2.把字符串转成datetime
# def string_toDatetime(st):
#     print("2.把字符串转成datetime: ", datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S"))

# # 3.把字符串转成时间戳形式
# def string_toTimestamp(st):
#     print("3.把字符串转成时间戳形式:", time.mktime(time.strptime(st, "%Y-%m-%d %H:%M:%S")))

# # 4.把时间戳转成字符串形式
# def timestamp_toString(sp):
#     print("4.把时间戳转成字符串形式: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sp)))

# # 5.把datetime类型转外时间戳形式
# def datetime_toTimestamp(dt):
#     print("5.把datetime类型转外时间戳形式:", time.mktime(dt.timetuple()))

# # 1.把datetime转成字符串
# datetime_toString(dt)
# # 2.把字符串转成datetime
# string_toDatetime(st)
# # 3.把字符串转成时间戳形式
# string_toTimestamp(st)
# # 4.把时间戳转成字符串形式
# timestamp_toString(sp)
# # 5.把datetime类型转外时间戳形式
# datetime_toTimestamp(dt)
