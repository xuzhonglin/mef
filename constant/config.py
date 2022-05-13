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

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
        print('加载配置文件成功')
except Exception as e:
    print('加载配置文件失败')
    raise e


def get_default(config: dict, key: str, default):
    """
    读取键值，如果没有，则返回默认值
    :param config: 配置
    :param key: 键值
    :param default: 默认值
    :return:
    """
    value = default
    env_key = 'MEF_' + key.upper()
    if key in config:
        value = config[key]
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


CLUSTER_NAME = get_default(config, 'cluster_name', 'lgh-sh1')
SERVER_PORT = get_default(config, 'server_port', 10282)
DEBUG_MODE = get_default(config, 'debug_mode', False)
LOG_PATH = get_default(config, 'log_path', 'logs')
LOG_LEVEL = get_default(config, 'log_level', 'INFO').upper()
REDIS_HOST = get_default(config, 'redis_host', 'localhost')
REDIS_PORT = get_default(config, 'redis_port', 6379)
REDIS_DB = get_default(config, 'redis_db', 0)
REDIS_USERNAME = get_default(config, 'redis_username', "")
REDIS_PASSWORD = get_default(config, 'redis_password', "")
REQUEST_LIMIT_PER_MINUTE = get_default(config, 'request_limit_per_minute', 120)
OCR_ENABLED = get_default(config, 'ocr_enabled', False)
OCR_SERVERS = get_default(config, 'ocr_servers', ["https://ocr.cotainer.colinxu.cn/"])
OCR_TIMEOUT = get_default(config, 'ocr_timeout', 5)
OCR_MAX_RETRY = get_default(config, 'ocr_max_retry', 3)
PROXY_ENABLED = get_default(config, 'proxy_enabled', False)
PROXY_SERVERS = get_default(config, 'proxy_servers', ["https://proxy01-mef.herokuapp.com/"])
PROXY_TIMEOUT = get_default(config, 'proxy_timeout', 5)
PROXY_MAX_RETRY = get_default(config, 'proxy_max_retry', 3)
PROXY_RULES = get_default(config, 'proxy_rules', {})
PROXY_PREFIX = get_default(config, 'proxy_prefix', "proxy")
PLAYER_SERVERS = get_default(config, 'player_servers', ["https://okjx.cc/?url="])
PLAYER_WEIGHTS = get_default(config, 'player_weights', [1])
PLAYER_RULES = get_default(config, 'player_rules', ["v.qq.com", "www.iqiyi.com",
                                                    "v.youku.com", "www.mgtv.com"])
LINE_EXCLUDE_RULES = get_default(config, 'line_exclude_rules', ["网盘", "云盘"])
