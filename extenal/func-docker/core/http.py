#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/4/27 21:10
@Author   : colinxu
@File     : http.py
@Desc     : http 请求
"""
import json
import random

import requests
from urllib3 import disable_warnings, exceptions
from urllib.parse import urlparse
from .log import Logger

disable_warnings(exceptions.InsecureRequestWarning)

logger = Logger(__name__).get_logger()


def http_get(url: str, params=None, headers: dict = None, timeout=5):
    """
    发送get请求
    :param url: URL地址
    :param params: 参数
    :param headers: 请求头
    :param timeout: 超时时间
    :return:
    """
    try:
        if url is None or not url.startswith('http'):
            raise Exception('url不合法')
        parsed_url = urlparse(url)
        headers = headers or {}
        # 添加固定header
        headers['Referer'] = parsed_url.scheme + '://' + parsed_url.netloc
        headers['User-Agent'] = _fake_ua()
        headers['Host'] = parsed_url.netloc

        # 发送请求
        return requests.get(url, params=params, headers=headers, timeout=timeout, verify=False)
    except Exception as e:
        logger.error('GET 请求异常原因：{}'.format(e))
        raise e


def http_post(url: str, data=None, headers: dict = None, timeout=5):
    """
    发送post请求
    :param url: URL地址
    :param data: 参数
    :param headers: 请求头
    :param timeout: 超时时间
    :return:
    """
    try:
        if url is None or not url.startswith('http'):
            raise Exception('url不合法')
        parsed_url = urlparse(url)
        headers = headers or {}
        # 添加固定header
        headers['Referer'] = parsed_url.scheme + '://' + parsed_url.netloc
        headers['User-Agent'] = _fake_ua()
        headers['Host'] = parsed_url.netloc
        if type(data) == dict:
            data = json.dumps(data)
            headers['Content-Type'] = 'application/json'
        else:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'

        # 发送请求
        return requests.post(url, data=data, headers=headers, timeout=timeout, verify=False)

    except Exception as e:
        logger.error('POST 请求异常原因：{}'.format(e))
        raise e


def _fake_ua():
    USER_AGENT_LIST = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_8 like Mac OS X) AppleWebKit/532.2 (KHTML, like Gecko) CriOS/34.0.877.0 Mobile/42D055 Safari/532.2",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 4.0; Trident/3.0)",
        "Mozilla/5.0 (Windows NT 6.2; fi-FI; rv:1.9.0.20) Gecko/2022-01-22 01:12:18 Firefox/7.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:1.9.6.20) Gecko/2020-02-07 16:48:35 Firefox/6.0",
        "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_11_7 rv:2.0; mhr-RU) AppleWebKit/532.22.5 (KHTML, like Gecko) Version/5.1 Safari/532.22.5",
        "Opera/9.41.(Windows NT 5.01; sw-TZ) Presto/2.9.177 Version/12.00",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1) AppleWebKit/534.46.6 (KHTML, like Gecko) Version/5.0.4 Safari/534.46.6",
        "Opera/8.66.(X11; Linux x86_64; ti-ER) Presto/2.9.170 Version/10.00",
        "Mozilla/5.0 (Windows 98; my-MM; rv:1.9.1.20) Gecko/2010-06-14 13:07:06 Firefox/3.6.9",
        "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 6.2; Trident/4.1)"
    ]
    return random.choice(USER_AGENT_LIST)
