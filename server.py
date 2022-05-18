#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/4/30 15:17
@Author   : colinxu
@File     : server.py
@Desc     : web服务器
"""
import json
import time

from flask import request, Response, send_from_directory

from service import MefService, ProxyService
from constant.config import SERVER_PORT, DEBUG_MODE
from util.auth import auth_login

app = ProxyService(__name__)

mef_service = MefService('source.json')


@app.route('/', methods=['GET'])
@app.route('/search', methods=['GET'])
@app.route('/detail', methods=['GET'])
@app.route('/admin/login', methods=['GET'])
def index():
    """
    主页
    :return:
    """
    return send_from_directory('static', 'index.html')


@app.route('/admin/source/list', methods=['GET'])
@app.route('/admin/source/edit', methods=['GET'])
@app.authorize_required
def admin():
    """
    主页
    :return:
    """
    return send_from_directory('static', 'index.html')


@app.route('/<path:path>')
def static_route(path):
    return send_from_directory('static', path)


@app.route('/api/login', methods=['POST'])
def admin_login():
    username = _parse_params('username')
    password = _parse_params('password')
    totp_code = _parse_params('totp_code')
    if _is_blank(username) or _is_blank(password) or _is_blank(totp_code):
        return _response(msg='用户名或密码或动态码不能为空', code=403)

    msg, auth_result = auth_login(username, password, totp_code)
    if not auth_result:
        return _response(msg=msg, code=403)

    cookie = {
        'mef_token': (msg, 60 * 60 * 7)
    }

    return _response('登陆成功', cookie=cookie)


@app.route('/api/source/<string:source_id>', methods=['GET'])
@app.authorize_required
def get_source(source_id):
    """
    获取数据源列表
    :return:
    """
    result = mef_service.get_source(source_id)
    return _response(result)


@app.route('/api/source/save', methods=['POST'])
@app.authorize_required
def save_source():
    """
    保存数据源
    :return:
    """
    body = _parse_params()
    ret = mef_service.verify_source(body)
    if str(ret).lower() != 'true':
        return _response(ret)
    return _response(mef_service.save_source(body))


@app.route('/api/source/import', methods=['POST'])
@app.authorize_required
def import_source():
    """
    导入数据源
    :return:
    """

    body = _parse_params()

    if _is_blank(body):
        return _response('参数不能为空')

    sources = []
    if isinstance(body, dict):
        sources.append(body)
    elif isinstance(body, list):
        sources = body

    for source in sources:
        ret = mef_service.verify_source(source)
        if str(ret).lower() != 'true':
            return _response(ret)

    return _response(mef_service.import_source(body))


@app.route('/api/source/verify', methods=['POST'])
@app.authorize_required
def verify_source():
    """
    校验数据源
    :return:
    """
    body = _parse_params()
    return _response(mef_service.verify_source(body))


@app.route('/api/test/search', methods=['POST'])
@app.authorize_required
def test_search():
    source = _parse_params('source')
    keyword = _parse_params('keyword')
    if source is None or keyword is None:
        return _response('参数不能为空')
    return _response(mef_service.test_search(source, keyword))


@app.route('/api/test/detail', methods=['POST'])
@app.authorize_required
def test_detail():
    """
    测试详情
    :return:
    """
    source = _parse_params('source')
    url = _parse_params('url')
    return _response(mef_service.test_detail(source, url))


@app.route('/api/test/play', methods=['POST'])
@app.authorize_required
def test_play():
    source = _parse_params('source')
    url = _parse_params('url')
    return _response(mef_service.test_play(source, url))


@app.route('/api/search', methods=['GET'])
def search():
    keyword = _parse_params('k')
    refresh = _parse_params('refresh')
    if keyword is None:
        return _response('搜索参数不能为空')
    refresh = _parse_bool(refresh)
    return _response(mef_service.search(keyword, refresh))


@app.route('/api/detail', methods=['GET', 'POST'])
def detail():
    source_id = _parse_params('id')
    detail_url = _parse_params('url')
    refresh = _parse_params('refresh')
    if _is_blank(source_id) or _is_blank(detail_url):
        return _response('参数不能为空')
    refresh = _parse_bool(refresh)
    return _response(mef_service.detail(source_id, detail_url, refresh))


@app.route('/api/play', methods=['GET', 'POST'])
def play():
    source_id = _parse_params('id')
    play_url = _parse_params('url')
    refresh = _parse_params('refresh')
    if _is_blank(source_id) or _is_blank(play_url):
        return _response('参数不能为空')
    refresh = _parse_bool(refresh)
    return _response(mef_service.play(source_id, play_url, refresh))


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


def _response(data=None, msg: str = 'success', code: int = 200, cookie: dict = None):
    ret = {
        'code': code,
        'msg': msg
    }
    if data is not None:
        ret['data'] = data

    response = Response(json.dumps(ret), mimetype='application/json')

    if cookie is not None:
        for k, v in cookie.items():
            value, expire = v
            response.set_cookie(k, value, expires=time.time() + expire)

    return response, 200


def _parse_params(name: str = None):
    if request.method == 'POST':
        if name is None:
            return request.json
        return request.json[name] if name in request.json else None
    elif request.method == 'GET':
        if name is None:
            return request.args
        return request.args.get(name) if name in request.args else None
    else:
        return None


def _parse_bool(s):
    try:
        if s is None:
            return False
        if isinstance(s, bool):
            return s
        return str(s) in ['true', '1', 'yes']
    except Exception as e:
        return False


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=SERVER_PORT, debug=DEBUG_MODE)
