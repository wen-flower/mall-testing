import functools
import time

import allure


def retry(count=5, delay=0):
    """
    配置失败重试
    :param count: 最多重试次数
    :param delay: 每次重试间隔时间，单位秒
    """
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 1
            while True:
                try:
                    with allure.step("第一次运行" if attempts == 1 else "第 %d 次尝试" % attempts):
                        return func(*args, **kwargs)
                except AssertionError as error:
                    attempts += 1
                    if attempts > count:
                        raise error
                    if delay > 0:
                        time.sleep(delay)

        return wrapper

    return decorator
