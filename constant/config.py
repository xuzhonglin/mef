#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/4/29 10:38
@Author   : colinxu
@File     : config.py
@Desc     : 系统配置
"""
import os
import json

RUN_ROLE = os.environ.get('MEF_RUN_ROLE', 'master')
CONFIG_KEY = 'MEF_CONFIG'
SOURCE_KEY = 'MEF_SOURCE'
MESSAGE_KEY = 'MEF_MESSAGE'

GLOBAL_CONFIG = {}


def get_default(data: dict, key: str, default):
    """
    读取键值，如果没有，则返回默认值
    :param data: 配置
    :param key: 键值
    :param default: 默认值
    :return:
    """
    value = default
    env_key = 'MEF_' + key.upper()
    if key in data:
        value = data[key]
    # 从环境变量中读取 环境变量>配置文件 MEF_xxx
    if env_key in os.environ:
        value = os.environ[env_key]
        if isinstance(default, bool):
            value = value.lower() in ['true', '1', 'yes']
        elif isinstance(default, int):
            value = int(value)
        elif isinstance(default, list):
            value = value.split(',')
    return value


if RUN_ROLE == 'master':
    # master
    try:
        print('MASTER 运行模式')
        with open('config.json', 'r') as f:
            GLOBAL_CONFIG = json.load(f)
            print('加载配置文件成功')
    except Exception as e:
        print('加载配置文件失败')
        raise e
elif RUN_ROLE == 'slave':
    # slave
    try:
        print('SLAVE 运行模式')
        import redis

        host = get_default(GLOBAL_CONFIG, 'redis_host', 'localhost')
        port = get_default(GLOBAL_CONFIG, 'redis_port', 6379)
        db = get_default(GLOBAL_CONFIG, 'redis_db', 0)
        username = get_default(GLOBAL_CONFIG, 'redis_username', "")
        password = get_default(GLOBAL_CONFIG, 'redis_password', "")
        REDIS = redis.Redis(host=host, port=port, db=db, username=username, password=password)
        REDIS.ping()
        config_temp = REDIS.get(CONFIG_KEY)
        if config_temp:
            GLOBAL_CONFIG = json.loads(config_temp)
            print('从 REDIS 加载配置文件成功')
            REDIS.close()

    except Exception as e:
        print('加载配置文件失败')
        raise e
else:
    raise Exception('配置文件错误')

SERVER_NAME = get_default(GLOBAL_CONFIG, 'server_name', 'master')
SERVER_PORT = get_default(GLOBAL_CONFIG, 'server_port', 10282)
DEBUG_MODE = get_default(GLOBAL_CONFIG, 'debug_mode', False)
LOG_PATH = get_default(GLOBAL_CONFIG, 'log_path', 'logs')
LOG_LEVEL = get_default(GLOBAL_CONFIG, 'log_level', 'INFO').upper()
REDIS_HOST = get_default(GLOBAL_CONFIG, 'redis_host', 'localhost')
REDIS_PORT = get_default(GLOBAL_CONFIG, 'redis_port', 6379)
REDIS_DB = get_default(GLOBAL_CONFIG, 'redis_db', 0)
REDIS_USERNAME = get_default(GLOBAL_CONFIG, 'redis_username', "")
REDIS_PASSWORD = get_default(GLOBAL_CONFIG, 'redis_password', "")
REQUEST_LIMIT_PER_MINUTE = get_default(GLOBAL_CONFIG, 'request_limit_per_minute', 120)
ADMIN_USERNAME = get_default(GLOBAL_CONFIG, 'admin_username', 'admin')
ADMIN_PASSWORD = get_default(GLOBAL_CONFIG, 'admin_password', 'admin')
ADMIN_SECRET = get_default(GLOBAL_CONFIG, 'admin_secret', 'admin')
OCR_ENABLED = get_default(GLOBAL_CONFIG, 'ocr_enabled', False)
OCR_SERVERS = get_default(GLOBAL_CONFIG, 'ocr_servers', ["https://ocr.cotainer.colinxu.cn/"])
OCR_TIMEOUT = get_default(GLOBAL_CONFIG, 'ocr_timeout', 5)
OCR_MAX_RETRY = get_default(GLOBAL_CONFIG, 'ocr_max_retry', 3)
PROXY_ENABLED = get_default(GLOBAL_CONFIG, 'proxy_enabled', False)
PROXY_SERVERS = get_default(GLOBAL_CONFIG, 'proxy_servers', ["https://proxy01-mef.herokuapp.com/"])
PROXY_TIMEOUT = get_default(GLOBAL_CONFIG, 'proxy_timeout', 5)
PROXY_MAX_RETRY = get_default(GLOBAL_CONFIG, 'proxy_max_retry', 3)
PROXY_RULES = get_default(GLOBAL_CONFIG, 'proxy_rules', {})
PROXY_PREFIX = get_default(GLOBAL_CONFIG, 'proxy_prefix', "proxy")
PLAYER_SERVERS = get_default(GLOBAL_CONFIG, 'player_servers', ["https://okjx.cc/?url="])
PLAYER_WEIGHTS = get_default(GLOBAL_CONFIG, 'player_weights', [1])
PLAYER_RULES = get_default(GLOBAL_CONFIG, 'player_rules', ["v.qq.com", "www.iqiyi.com",
                                                           "v.youku.com", "www.mgtv.com"])
LINE_EXCLUDE_RULES = get_default(GLOBAL_CONFIG, 'line_exclude_rules', ["网盘", "云盘"])
