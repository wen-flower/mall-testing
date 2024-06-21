import enum
from typing import Callable, List

import allure
from allure_commons.types import Severity
from requests import Response

from utils.assertion import assert_eq


class BaseCase:

    def __init__(self,
                 case_id: str, case_url: str,
                 body: dict = None, status_code: int = 200,
                 validators: List[Callable] = None,
                 level: Severity = allure.severity_level.NORMAL):
        self.case_id = case_id
        self.case_url = case_url
        self.body = body
        self.status_code = status_code
        self.level = level

        self.validators = [
            lambda resp: assert_eq(resp.status_code, self.status_code),
        ]

        self.validators.extend(validators)

    def __repr__(self):
        return self.case_id

    def severity(self, level: Severity = allure.severity_level.NORMAL):
        self.level = level
        return self

    def setup(self):
        """初始设置"""
        allure.dynamic.severity(allure.severity_level.CRITICAL)
        allure.dynamic.testcase(self.case_url, self.case_id)
        if self.body is not None:
            allure.dynamic.parameter("请求 Body", self.body, excluded=True)

    def teardown(self, resp: Response):
        """验证请求结果"""
        for validator in self.validators:
            validator(resp)
