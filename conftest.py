import allure
import pytest

import common


@allure.title("初始化全局配置类：Config")
@pytest.fixture
def config():
    return common.config.load()
