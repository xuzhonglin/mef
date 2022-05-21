#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/5/11 18:05
@Author   : colinxu
@File     : redis.py
@Desc     : 缓存模块
"""
import redis
import json

from hashlib import md5
from util.logging import Logger
from constant.config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB, REDIS_USERNAME, RUN_ROLE, CONFIG_KEY, \
    GLOBAL_CONFIG

logger = Logger(__name__).get_logger()

try:
    REDIS = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, username=REDIS_USERNAME,
                        password=REDIS_PASSWORD)
    REDIS.ping()
    logger.info(
        "Redis连接成功,redis://{}:{}@{}:{}/{}".format(REDIS_USERNAME, REDIS_PASSWORD, REDIS_HOST, REDIS_PORT, REDIS_DB))
    if RUN_ROLE == "master":
        logger.info("当前主机为主节点,已经自动设置配置缓存")
        REDIS.set(CONFIG_KEY, json.dumps(GLOBAL_CONFIG))
except Exception as e:
    REDIS = None
    logger.error(
        'redis连接失败，请检查配置！redis://{}:{}@{}:{}/{}'.format(REDIS_USERNAME, REDIS_PASSWORD, REDIS_HOST, REDIS_PORT,
                                                        REDIS_DB))
    exit(-1)


def get_redis():
    if REDIS is None:
        logger.info('redis连接失败，请检查配置！')
        return None
    return REDIS


def parse_key(*args):
    key_array = []
    for arg in args:
        if isinstance(arg, str):
            if arg.startswith('http'):
                key_array.append(md5(arg.encode('utf-8')).hexdigest().upper())
            else:
                key_array.append(arg.upper())
        elif isinstance(arg, int):
            key_array.append(str(arg))
    return '_'.join(key_array)


def parse_value(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return value
