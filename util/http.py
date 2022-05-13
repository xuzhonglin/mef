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

from util.common import fake_ua
from util.logging import Logger
from constant.config import PROXY_SERVERS, PROXY_ENABLED, PROXY_TIMEOUT

disable_warnings(exceptions.InsecureRequestWarning)

logger = Logger(__name__).get_logger()


def http_get(url, params=None, headers: dict = None, timeout=5):
    """
    发送get请求
    :param url: URL地址
    :param params: 参数
    :param headers: 请求头
    :param timeout: 超时时间
    :return:
    """
    try:
        parsed_url = urlparse(url)
        # 添加固定header
        headers['Referer'] = parsed_url.scheme + '://' + parsed_url.netloc
        headers['User-Agent'] = fake_ua()
        headers['Host'] = parsed_url.netloc

        # 发送请求
        if PROXY_ENABLED:
            return proxy_request(url, 'GET', params=params, headers=headers, timeout=PROXY_TIMEOUT)
        else:
            return requests.get(url, params=params, headers=headers, timeout=timeout, verify=False)
    except Exception as e:
        logger.error('GET 请求异常：代理：{}，原因：{}'.format(PROXY_ENABLED, e))
        # delete_proxy_ip(proxy_ip)
        raise e


def http_post(url, data=None, headers: dict = None, timeout=5):
    """
    发送post请求
    :param url: URL地址
    :param data: 参数
    :param headers: 请求头
    :param timeout: 超时时间
    :return:
    """
    try:
        parsed_url = urlparse(url)
        # 添加固定header
        headers['Referer'] = parsed_url.scheme + '://' + parsed_url.netloc
        headers['User-Agent'] = fake_ua()
        headers['Host'] = parsed_url.netloc
        if type(data) == dict:
            data = json.dumps(data)
            headers['Content-Type'] = 'application/json'
        else:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'

        # 发送请求
        if PROXY_ENABLED:
            return proxy_request(url, 'POST', data=data, headers=headers, timeout=PROXY_TIMEOUT)
        else:
            return requests.post(url, data=data, headers=headers, timeout=timeout, verify=False)

    except Exception as e:
        logger.error('POST 请求异常：代理：{}，原因：{}'.format(PROXY_ENABLED, e))
        # logger.error('发送post请求异常：{}，代理IP：{}'.format(e, proxy_ip))
        # delete_proxy_ip(proxy_ip)
        raise e


def proxy_request(url, method: str = 'GET', params=None, data=None, headers: dict = None, timeout=5):
    """
    发送请求
    :param url:
    :param params:
    :param headers:
    :param timeout:
    :return:
    """
    proxy_server = get_proxy()
    payload = {
        'url': url,
        'method': method,
        'params': params,
        'data': data,
        'headers': headers,
        'timeout': timeout
    }
    headers = {'Content-Type': 'application/json'}
    return requests.post(proxy_server, data=json.dumps(payload), headers=headers, timeout=timeout)


def session():
    """
    返回session对象
    :return:
    """
    return requests.session()


def get_proxy(scheme='http'):
    """
    获取代理
    """
    # try:
    #     url = PROXY_POOL + 'get/?type=' + scheme
    #     resp = requests.get(url, verify=False, timeout=2)
    #     if resp.status_code == 200:
    #         proxy = resp.json()['proxy']
    #         if proxy:
    #             return proxy
    # except Exception as e:
    #     logger.error('获取代理IP异常：{}'.format(e))
    # return None

    return random.choice(PROXY_SERVERS)


def delete_proxy_ip(proxy):
    """
    删除代理
    """
    # try:
    #     url = PROXY_POOL + 'delete/?proxy={}'.format(proxy)
    #     resp = requests.get(url, verify=False, timeout=2)
    #     if resp.status_code == 200:
    #         logger.info('删除代理IP：{}'.format(proxy))
    # except Exception as e:
    #     logger.error('删除代理IP异常：{}'.format(e))
