#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/4/30 15:17
@Author   : colinxu
@File     : server.py
@Desc     : web服务器
"""
import json
from functools import wraps

from flask import request, Response, send_from_directory, redirect
from flask_basicauth import BasicAuth

from service import MefService, ProxyService
from constant.config import SERVER_PORT, DEBUG_MODE

app = ProxyService(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'colinxu'
app.config['BASIC_AUTH_PASSWORD'] = 'colin2why**'

mef_service = MefService('source.json')
basic_auth = BasicAuth(app)


def authorized_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # request_token = request.headers.get('Token')
        # if _is_blank(request_token):
        #     return redirect('/')
        return f(*args, **kwargs)

    return decorated_function


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    主页
    :return:
    """
    return app.send_static_file('index.html')


@app.route('/admin', methods=['GET'])
@basic_auth.required
def source_manage():
    return redirect('/#/source/index')


@app.route('/<path:path>')
def static_route(path):
    return send_from_directory('static', path)


@app.route('/api/source/<string:source_id>', methods=['GET'])
@authorized_only
@basic_auth.required
def get_source(source_id):
    """
    获取数据源列表
    :return:
    """
    result = mef_service.get_source(source_id)
    return _response(result)


@app.route('/api/source/save', methods=['POST'])
@authorized_only
@basic_auth.required
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
@authorized_only
@basic_auth.required
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
@authorized_only
@basic_auth.required
def verify_source():
    """
    校验数据源
    :return:
    """
    body = _parse_params()
    return _response(mef_service.verify_source(body))


@app.route('/api/test/search', methods=['POST'])
@authorized_only
@basic_auth.required
def test_search():
    source = _parse_params('source')
    keyword = _parse_params('keyword')
    if source is None or keyword is None:
        return _response('参数不能为空')
    return _response(mef_service.test_search(source, keyword))


@app.route('/api/test/detail', methods=['POST'])
@authorized_only
@basic_auth.required
def test_detail():
    """
    测试详情
    :return:
    """
    source = _parse_params('source')
    url = _parse_params('url')
    return _response(mef_service.test_detail(source, url))


@app.route('/api/test/play', methods=['POST'])
@authorized_only
@basic_auth.required
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


def _response(data=None, msg: str = 'success', code: int = 200):
    ret = {
        'code': code,
        'msg': msg
    }
    if data is not None:
        ret['data'] = data

    response = Response(json.dumps(ret), mimetype='application/json')

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
