"""字符串处理的常用函数"""


def add_char_until_length(string, n, char=" "):
    """给定一个字符串，通过在字符串开头加入若干个空格(或其它字符char)，
    使得输出字符串的长度为n"""
    if len(string) >= n:
        return string  # 如果字符串长度已经大于等于N，则直接返回原字符串
    spaces_added = char * (n - len(string))
    return spaces_added + string
