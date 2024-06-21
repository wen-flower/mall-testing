from typing import Callable, TypeVar


def assert_eq(expected, actual):
    try:
        assert expected == actual
    except AssertionError:
        raise AssertionError("预期值：%s，实际值：%s" % (expected, actual))


def assert_type(expected, value):
    try:
        assert isinstance(value, expected)
    except AssertionError:
        raise AssertionError("预期类型：%s，实际类型：%s" % (expected, type(value)))


R = TypeVar('R')


class AssertChain:

    def __init__(self, obj):
        if isinstance(obj, AssertChain):
            self.obj = obj.obj
        else:
            self.obj = obj

    def map(self, run: Callable[[object], 'AssertChain']) -> 'AssertChain':
        """修改链类型"""
        return AssertChain(run(self.obj))

    def child(self, run: Callable[['AssertChain'], None]) -> 'AssertChain':
        run(self)
        return self

    def type(self, expected_type):
        if isinstance(self.obj, expected_type):
            return self
        raise AssertionError("预期类型：%s，实际类型：%s，值：%s" % (expected_type, type(self.obj), self.obj))

    def eq(self, expected_value):
        if self.obj == expected_value:
            return self
        raise AssertionError("预期值：%s，实际值：%s" % (expected_value, self.obj))

    def len(self, expected_length: int):
        if len(self.obj) == expected_length:
            return self
        raise AssertionError("预期长度：%d，实际长度：%d，值：%s" % (expected_length, len(self.obj), self.obj))
