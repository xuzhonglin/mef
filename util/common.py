#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/4/27 20:44
@Author   : colinxu
@File     : common.py
@Desc     : 公共工具类
"""

import random
import json

from bs4.element import Tag
from urllib.parse import urlparse

from constant.user_agent import *


def fake_ua():
    """
    随机获取一个user-agent
    :return:
    """
    return random.choice(USER_AGENT_LIST)


def parse_url(url: str):
    """
    解析url
    :param url:
    :return:
    """
    if url is None:
        return None
    else:
        return urlparse(url)


def is_empty(value):
    """
    判断是否为空
    :param value:
    :return:
    """
    if value is None:
        return True
    elif isinstance(value, str):
        return value.strip() == ''
    elif isinstance(value, list):
        return len(value) == 0
    elif isinstance(value, dict):
        return len(value) == 0
    else:
        return False


def get_attr(tag: Tag, pattern: str):
    """
    获取属性值
    :param tag: 标签
    :param pattern: 模式
    :return:
    """
    pattern = pattern.strip()
    if "@" not in pattern:
        if pattern == "text":
            value = tag.text
        else:
            value = tag.get(pattern)
    else:
        sub_patterns = pattern.split('@')
        selector, attr_name = sub_patterns[0].strip(), sub_patterns[1].strip()
        element = tag.select_one(selector)
        if element is None:
            return None

        if attr_name == 'text':
            value = tag.select_one(selector).text
        else:
            value = tag.select_one(selector).get(attr_name)

    return None if is_empty(value) else value.strip()


def complete_url(host: str, url: str):
    """
    完善url
    :param host: 主机名
    :param url:url
    :return:
    """
    if url is None or type(url) != str:
        return None
    if url.startswith('http'):
        return url
    else:
        return host + url


def is_valid_json(json_str):
    """
    判断是否为json
    :param json_str:
    :return:
    """
    try:
        if type(json_str) == str:
            json_obj = json.loads(json_str)
            return True
        elif type(json_str) == dict:
            return True
    except Exception as e:
        return False
