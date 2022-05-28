#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/5/10 10:36
@Author   : colinxu
@File     : proxy.py
@Desc     : 代理服务器
"""
import base64
import re
import os
import json
import requests

from flask import Flask, request, Response, render_template, send_from_directory
from flask_cors import CORS
from urllib3 import disable_warnings, exceptions
from urllib.parse import urlparse
from core.player import Player
from core.log import Logger

app = Flask(__name__)
disable_warnings(exceptions.InsecureRequestWarning)

CORS(app, supports_credentials=True)

logger = Logger(__name__).get_logger()


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


@app.route('/<path:path>')
def static_route(path):
    return send_from_directory('static', path)


@app.route('/player')
def player():
    play_url = _parse_params('url')

    if _is_blank(play_url):
        return _response(msg='Url required')

    if not play_url.startswith('http'):
        play_url = base64.b64decode(play_url).decode('utf-8')

    if play_url.startswith('https://www.libvio.me'):
        config = {
            'siteInfo': 'head > script|5 @ text $ replace:"","/proxy/player/www.libvio.me"',
            'playerConfig': '.embed-responsive clearfix @ content $ replace:/static,/proxy/player/www.libvio.me/static'
        }
    elif play_url.startswith('https://www.tkys.tv'):
        config = {
            'siteInfo': 'head > script|0 @ text $ replace:"","//www.tkys.tv"',
            'playerConfig': '.embed-responsive clearfix @ content $ replace:/static,//www.tkys.tv/static'
        }
    elif play_url.startswith('https://www.lgyy.cc'):
        config = {
            'siteInfo': 'body > script|0 @ text $ replace:"","//www.lgyy.cc"',
            'playerConfig': '.player-box-main @ content $ replace:/static,//www.lgyy.cc/static'
        }
    elif play_url.startswith('https://www.zxzjtv.com'):
        config = {
            'siteInfo': 'head > script|5 @ text $ replace:"","/proxy/player/www.zxzjtv.com"',
            'playerConfig': '.stui-player__video clearfix @ content $ replace:/static,//www.zxzjtv.com/static'
        }
    elif play_url.startswith('https://www.jubaibai.cc'):
        config = {
            'siteInfo': 'head > script|6 @ text $ replace:"","/proxy/player/www.jubaibai.cc"',
            'playerConfig': '.stui-player__video @ content $ replace:/static,//www.jubaibai.cc/static'
        }
    elif play_url.startswith('https://www.5dy5.cc'):
        config = {
            'siteInfo': 'head > script|0 @ text $ replace:"","/proxy/player/www.5dy5.cc"',
            'playerConfig': '.embed-responsive clearfix @ content $ replace:/static,//www.5dy5.cc/static'
        }
    else:
        return _response(msg='Unsupported Url')
    player_parse = Player(play_url, config)
    site_info = player_parse.get_site_info()
    player_config = player_parse.get_player_config()
    return render_template('player.html', site_info=site_info, player_config=player_config)


@app.before_request
def proxy_player():
    if request.path.startswith('/proxy/player'):
        return player_proxy_handler()


def player_proxy_handler():
    replacements = []
    url = request.path.replace('/proxy/player/', '')
    if not url.startswith('http'):
        url = 'https://' + url
    elif url.startswith('https:'):
        url = re.sub(r'http[s]?:[\/]+', 'https://', url)
    elif url.startswith('http:'):
        url = re.sub(r'http[s]?:[\/]+', 'https://', url)

    headers = _unpack_headers(request.headers)
    parse_result = urlparse(url)
    headers["Host"] = parse_result.netloc
    headers["Referer"] = parse_result.scheme + '://' + parse_result.netloc

    dir_replaces = [
        ['/Content', '/Content', '{}://{}/Content'.format(parse_result.scheme, parse_result.netloc)],
        ['/Scripts', '/Scripts', '{}://{}/Scripts'.format(parse_result.scheme, parse_result.netloc)],
        ['/ParsePlayer', '/ParsePlayer',
         '{}://{}/ParsePlayer'.format(parse_result.scheme, parse_result.netloc)]
    ]

    replacements.extend(dir_replaces)

    if parse_result.path.startswith('/static/player'):
        player_replaces = [
            ['src="', 'src="/proxy/player/'],
            ["?", "PlayUrl", "PlayUrl+'&referer={}'".format(headers['Referer']),
             "PlayUrl+'?referer={}'".format(headers['Referer'])]
        ]
        replacements.extend(player_replaces)

    if 'referer' in request.args:
        headers["Referer"] = request.args.get('referer')

    headers['Accept-Encoding'] = 'gzip'

    response = requests.request(method=request.method, url=url, headers=headers, data=request.form,
                                params=request.args, verify=False, timeout=5)

    response_headers = _unpack_headers(response.headers)

    response_headers.pop('Server', None)
    response_headers.pop('Date', None)
    response_headers.pop('Content-Length', None)
    response_headers.pop('Content-Encoding', None)
    response_headers.pop('Transfer-Encoding', None)
    response_headers.pop('Connection', None)

    content_type = response.headers["Content-Type"] if "Content-Type" in response.headers else ""

    need_replace = len(replacements) > 0 and ('html' in content_type or 'javascript' in content_type)

    # 排除指定后缀
    ignore_suffix = ['playerconfig.js', 'player.js']

    for ignore_item in ignore_suffix:
        if ignore_item in url:
            need_replace = False
            break

    # 解决乱码问题
    if 'Content-Encoding' in response.headers and response.headers['Content-Encoding'] != 'gzip':
        response_headers['Content-Encoding'] = response.headers['Content-Encoding']

    if not need_replace:
        return response.content, response.status_code, response_headers

    try:
        response_text = response.content.decode(encoding="utf-8")
    except Exception as e:
        logger.error('编码解析异常：{}'.format(request.full_path))
        logger.error(e)
        logger.info(response.headers)
        response_text = response.text
        logger.info(response_text)

    # 执行替换操作
    for replacement_item in replacements:

        if len(replacement_item) == 4:
            old = replacement_item[1]
            new = replacement_item[2] if replacement_item[0] in response_text else replacement_item[3]
        elif len(replacement_item) == 3:
            old = replacement_item[1]
            new = replacement_item[2] if replacement_item[0] in response_text else replacement_item[0]
        else:
            old = replacement_item[0]
            new = replacement_item[1]

        # 带参数替换
        new_temp = new.replace("'", "")
        if new_temp.startswith('{') and new_temp.endswith('}'):
            new = new.format(**request.args)

        if old.startswith('reg:'):
            old = old[4:]
            response_text = re.sub(old, new, response_text)
        else:
            response_text = response_text.replace(old, new, 1)

    return response_text, response.status_code, response_headers


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
