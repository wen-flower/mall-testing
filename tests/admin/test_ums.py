import allure
import pytest
from requests import post

from utils import retry
from ums import login_test_case


@retry()
@allure.parent_suite("Mall后台系统")
@allure.suite("后台用户管理")
@allure.title("登录接口测试")
@pytest.mark.parametrize("case", login_test_case.build(), ids=lambda p: repr(p))
def test_login(config, case):
    case.setup()
    resp = post(config.url("/admin/login"), json=case.body)

    case.teardown(resp)
