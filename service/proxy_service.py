#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/5/2 14:43
@Author   : colinxu
@File     : proxy_service.py
@Desc     : 代理服务
"""
import datetime
import logging
import re
import time
import uuid

import requests

from flask import Flask, request, Response
from flask_cors import CORS
from urllib.parse import urlparse

from util.logging import Logger
from util.redis import get_redis, parse_key
from constant.config import PROXY_RULES, REQUEST_LIMIT_PER_MINUTE, DEBUG_MODE

logger = Logger(__name__).get_logger()

Redis = get_redis()


class ProxyService(Flask):

    def __init__(self, *args, **kwargs):
        super(ProxyService, self).__init__(*args, **kwargs)
        self.logger = logger
        self._setup_logging()
        self._setup_reverse_proxy()
        if DEBUG_MODE:
            logger.info("调试模式开启，允许跨域请求")
            CORS(self, supports_credentials=True)
        logger.info("ProxyService init success")

    def __del__(self):
        logger.info("ProxyService stopped")

    def _setup_logging(self):
        """
        设置日志 重新定义日志输出格式
        :return:
        """
        werkzeug_logger = logging.getLogger('werkzeug')
        werkzeug_logger.handlers.clear()
        for handler in self.logger.handlers:
            werkzeug_logger.addHandler(handler)
        logger.info("ProxyService logging setup success")

    def _setup_reverse_proxy(self):
        """
        设置反向代理
        :return:
        """
        self.before_request(self._before_request)
        self.after_request(self._before_response)

    def _before_request(self):
        """
        反向代理处理
        :return:
        """
        # if request.url_rule is not None:
        #     url_rule = request.url_rule
        #     endpoint = url_rule.endpoint
        #     return self.view_functions[endpoint](**request.view_args, **request.args, **request.form)
        #
        # path = request.path
        # if path.startswith("/proxy"):
        #     self.logger.info("ProxyService reverse proxy handle")
        #     return self._reverse_proxy_handle()

        request_id = request.cookies.get('mef_request_id')

        # 图片请求不做限制
        if not request.path.startswith('/proxy/image') and request_id is not None:
            cache_name = parse_key('REQUEST', request_id)
            cache_key = request.path
            last_request_time = Redis.hget(cache_name, cache_key)
            if last_request_time is None:
                Redis.hset(cache_name, cache_key, time.time())
                Redis.expire(cache_name, 60 * 60 * 12)
            else:
                last_request_time = float(last_request_time)
                request_time = time.time()
                # 判断是否超过限制
                if request_time - last_request_time <= 60 / REQUEST_LIMIT_PER_MINUTE:
                    return Response(status=403)
                Redis.hset(cache_name, cache_key, request_time)

        if request.url_rule is None or request.endpoint == "static_route":
            path = request.path
            if path.startswith("/proxy"):
                self.logger.debug("ProxyService reverse proxy handle")
                return self._reverse_proxy_handle()

    def _before_response(self, response: Response):
        """
        响应前处理
        :return:
        """
        if 'mef_request_id' not in request.cookies:
            request_id = str(uuid.uuid4()).replace('-', '')
            response.set_cookie('mef_request_id', request_id, max_age=60 * 60 * 24 * 7)
        return response

    def _reverse_proxy_handle(self):
        """
        代理处理
        :return:
        """

        path_array = request.path.split("/")
        target = path_array[2]

        if target in PROXY_RULES:
            target_config = PROXY_RULES[target]
            url = '/' + '/'.join(path_array[3:]) + '?' + request.query_string.decode()
            host = target_config['host']
            if host == '*':
                url = request.args.get('url')
                host = urlparse(url).scheme + '://' + urlparse(url).netloc
                headers = self._unpack_headers(request.headers)
                headers.update(target_config["headers"])
                headers["Host"] = urlparse(host).netloc
                headers["Referer"] = host
            else:
                url = host + url
                headers = self._unpack_headers(request.headers)
                headers.update(target_config["headers"])
                headers["Host"] = urlparse(host).netloc

            # headers["X-Real-IP"] = request.remote_addr
            # headers["X-Forwarded-For"] = request.remote_addr
            # headers["REMOTE_ADDR"] = request.remote_addr

            response = requests.request(method=request.method, url=url, headers=headers, data=request.form,
                                        params=request.args, verify=False, timeout=5)
            response_headers = {}
            content_type = response.headers["Content-Type"] if "Content-Type" in response.headers else ""
            if content_type != "":
                response_headers["Content-Type"] = content_type
            replacements = target_config["replacements"]
            need_replace = len(replacements) > 0 and 'text' in content_type
            if not need_replace:
                return response.content, response.status_code, response_headers
            response_text = response.content.decode(encoding="utf-8")
            for replacement in replacements:
                old = replacement[0]
                new = replacement[1]
                # 带参数替换
                new_temp = new.replace("'", "")
                if new_temp.startswith('{') and new_temp.endswith('}'):
                    new = new.format(**request.args)

                if old.startswith('reg:'):
                    old = old[4:]
                    response_text = re.sub(old, new, response_text)
                else:
                    response_text = response_text.replace(old, new)
            return response_text, response.status_code, response_headers

    def _unpack_headers(self, headers):
        """
        解包headers
        :param headers:
        :return:
        """
        header_dict = {}
        for key, value in headers.items():
            header_dict[key] = value
        return header_dict

    def run(self, *args, **kwargs):
        """
        启动服务
        :param args:
        :param kwargs:
        :return:
        """
        logger.info("ProxyService started at {}:{}".format(kwargs.get("host"), kwargs.get("port")))
        # proxyConfig.LOCAL_HOST = "http://{}:{}".format(kwargs.get("host"), kwargs.get("port"))
        super(ProxyService, self).run(*args, **kwargs)
