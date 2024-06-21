from typing import Callable

import allure
from jsonpath import jsonpath

from common import BaseCase
from utils.assertion import AssertChain


def build():
    return [
        LoginTestCase(
            "ADMIN_USER_000001", "https://www.kdocs.cn/l/cjwsebgDw01q?R=L0MvNS9I",
            "admin", "macro123",
            [
                lambda resp: AssertChain(resp.json()).map(lambda data: jsonpath(data, "$.data.token"))
                .type(list).len(1).map(lambda obj: obj[0]).type(str),
            ],
        ).severity(allure.severity_level.BLOCKER),
        LoginTestCase(
            "ADMIN_USER_000002", "https://www.kdocs.cn/l/cjwsebgDw01q?R=L0MvNS9Q",
            "admintest", "macro123456",
            [
                lambda resp: AssertChain(resp.json()).map(lambda data: jsonpath(data, "$.message"))
                .type(list).len(1).map(lambda obj: obj[0]).type(str).eq("用户名或密码错误"),
            ]
        ),
        LoginTestCase(
            "ADMIN_USER_000003", "https://www.kdocs.cn/l/cjwsebgDw01q?R=L0MvNS9R",
            "admin", "",
            [
                lambda resp: AssertChain(resp.json()).map(lambda data: jsonpath(data, "$.message"))
                .type(list).len(1).map(lambda obj: obj[0]).type(str).eq("password不能为空"),
            ]
        ),
        LoginTestCase(
            "ADMIN_USER_000004", "https://www.kdocs.cn/l/cjwsebgDw01q?R=L0MvNS9S",
            "", "macro123",
            [
                lambda resp: AssertChain(resp.json()).map(lambda data: jsonpath(data, "$.message"))
                .type(list).len(1).map(lambda obj: obj[0]).type(str).eq("username不能为空"),
            ]
        ),
        LoginTestCase(
            "ADMIN_USER_000005", "https://www.kdocs.cn/l/cjwsebgDw01q?R=L0MvNS9T",
            "admin", "macro123456",
            [
                lambda resp: AssertChain(resp.json()).map(lambda data: jsonpath(data, "$.message"))
                .type(list).len(1).map(lambda obj: obj[0]).type(str).eq("密码不正确"),
            ]
        ),
    ]


class LoginTestCase(BaseCase):

    def __init__(self, case_id: str, case_url: str, username: str, password: str,
                 validators: list[Callable]):
        super().__init__(
            case_id,
            case_url,
            {
                "username": username,
                "password": password
            },
            validators=validators,
        )
