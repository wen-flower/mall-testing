import logging

import yaml
from jsonpath import jsonpath


class ParseConfigError(BaseException):

    def __init__(self, message):
        super().__init__(message)


class Config:

    def __init__(self, config: dict):
        self.config = config

    def url(self, path=""):
        """
        获取测试使用的基础地址
        """
        host = jsonpath(self.config, "host")
        if host is False:
            host = "http://localhost:8080"
            logging.warning("use default host %s" % host)
        else:
            host = host[0]
            if not isinstance(host, str):
                raise ParseConfigError("host 要求一个 URL 字符串")
        return host + path


def load(path="./config.yaml"):
    with open(path, "r") as file:
        return Config(yaml.safe_load(file))
