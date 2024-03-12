"""用于logging中打印输出join起来的字符串"""


class LazyJoin:
    """用于logging中打印输出join起来的字符串
    使用案例：
    logger.debug(
    'Stupid log message %s', lazyjoin(' ', (str(i) for i in range(20)))
    )
    """

    def __init__(self, s, items):
        self.s = s
        self.items = items

    def __str__(self):
        return self.s.join(self.items)
