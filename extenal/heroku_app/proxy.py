#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/5/10 10:36
@Author   : colinxu
@File     : proxy.py
@Desc     : 代理服务器
"""
import os
import json
import logging
import requests

from flask import Flask, request, Response
from flask_cors import CORS
from urllib3 import disable_warnings, exceptions

app = Flask(__name__)
logger = logging.getLogger('proxy')
disable_warnings(exceptions.InsecureRequestWarning)

CORS(app, supports_credentials=True)

logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)7s - %(threadName)10s - %(module)15s.%(funcName)15s : %(message)s')

# 控制台日志
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


@app.route('/', methods=['GET', 'POST'])
def handle_request():
    if request.method == 'GET':
        logger.info('检测到 GET 请求')
        return _response(msg='Hello, World!', code=200)
    elif request.method == 'POST':
        body = _parse_params()
        if _is_blank(body) is None:
            return _response(msg='body is blank', code=400)
        return handle_proxy(body)


def handle_proxy(body: dict):
    url = body['url'] if 'url' in body else None
    method = body['method'] if 'method' in body else None
    headers = body['headers'] if 'headers' in body else None
    params = body['params'] if 'params' in body else None
    data = body['data'] if 'data' in body else None
    timeout = body['timeout'] if 'timeout' in body else None

    if _is_blank(url):
        return _response(msg='url is blank', code=400)
    if _is_blank(method):
        return _response(msg='method is blank', code=400)

    logger.info('检测到请求：{}, 方式：{}'.format(url, method))

    try:
        if url is None or not url.startswith('http'):
            raise Exception('url不合法')
        if method == 'GET':
            resp = requests.get(url=url, headers=headers, params=params, timeout=timeout, verify=False)
        else:
            resp = requests.post(url=url, headers=headers, params=params, data=data, timeout=timeout, verify=False)

        resp_headers = _unpack_headers(resp.headers)

        resp_headers.pop('Server', None)
        resp_headers.pop('Date', None)
        resp_headers.pop('Content-Length', None)
        resp_headers.pop('Content-Encoding', None)
        resp_headers.pop('Transfer-Encoding', None)
        resp_headers.pop('Connection', None)

        logger.info('响应成功：{}'.format(url))

        return Response(resp.content, headers=resp_headers, status=resp.status_code)
    except Exception as e:
        print(e)
        logger.error('请求异常：{}，{}'.format(url, e))
        return _response(msg='proxy error', code=500)


def _is_blank(s):
    if s is None:
        return True
    elif type(s) == int:
        return s is None
    elif type(s) == str:
        return s is None or len(s) == 0
    elif type(s) == list:
        return len(s) == 0
    elif type(s) == dict:
        return len(s) == 0


def _response(data=None, msg: str = 'success', code: int = 200):
    ret = {
        'code': code,
        'msg': msg
    }
    if data is not None:
        ret['data'] = data

    return Response(json.dumps(ret), mimetype='application/json'), 200


def _parse_params(name: str = None):
    if request.method == 'POST':
        if name is None:
            return request.json
        return request.json[name]
    elif request.method == 'GET':
        return request.args.get(name)
    else:
        return None


def _unpack_headers(headers):
    ret = {}
    if headers is None:
        return ret
    for k, v in headers.items():
        ret[k] = v
    return ret


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10284))
    app.run(host='0.0.0.0', port=port)
