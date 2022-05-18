#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/4/29 13:20
@Author   : colinxu
@File     : service.py
@Desc     : 服务层
"""
import json
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

from model.source import Source
from parser.result_parser import ResultParser
from parser.detail_parser import DetailParser
from parser.play_parser import PlayParser
from util.common import parse_url, is_valid_json
from util.logging import Logger
from constant.source_keys import SourceKeys
from constant.config import RUN_ROLE, SOURCE_KEY, MESSAGE_KEY, SERVER_NAME
from util.redis import get_redis, parse_key, parse_value

MAX_WORKERS = 10

logger = Logger(__name__).get_logger()

Redis = get_redis()


class MefService:

    def __init__(self, path: str):
        self.path = path
        self.origin_source_map = {}
        self.origin_source_list = []
        self.result_parsers = self._load_source()

        max_workers = min(MAX_WORKERS, len(self.result_parsers))
        max_workers = max(max_workers, 1)
        logger.info('初始化线程池, 最大线程数 {}'.format(max_workers))
        self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)

    def get_source(self, source_id: str = None):
        """
        获取资源
        :return:
        """
        if source_id is None or source_id == 'list':
            return [source_item for source_item in self.origin_source_map.values()]
        if source_id in self.origin_source_map:
            return self.origin_source_map[source_id]
        return None

    def import_source(self, sources: (list, dict)):
        """
        导入资源
        :param sources:
        :return:
        """
        if isinstance(sources, dict):
            return self.save_source(sources)
        elif isinstance(sources, list):
            for source in sources:
                ret = self.save_source(source)
                if not ret:
                    return False
            return True
        return False

    def save_source(self, source: dict, skip_message: bool = False):
        """
        保存资源
        :param source:
        :return:
        """
        try:
            source_id = source['sourceId']
            if source_id not in self.origin_source_map:
                logger.info('资源 {} 不存在，新增'.format(source_id))
                self.origin_source_map[source_id] = source
            else:
                logger.info('资源 {} 存在，更新'.format(source_id))
                self.origin_source_map[source_id].update(source)

            self.origin_source_list = []
            for source_item in self.origin_source_map.values():
                self.origin_source_list.append(source_item)
            logger.info('资源列表更新成功')

            Redis.set(SOURCE_KEY, parse_value(self.origin_source_list))
            logger.info('资源更新 Redis 成功')

            if RUN_ROLE == 'master':
                with open(self.path, 'w') as f:
                    json.dump(self.origin_source_list, f, indent=4, ensure_ascii=False)
                logger.info('保存本地资源成功')

            if not skip_message:
                logger.info('发送 Source 更新消息')
                message = {
                    'message_id': uuid.uuid4().hex,
                    'message_content': 'source_update',
                    'message_from': SERVER_NAME
                }
                recv_cnt = Redis.publish(MESSAGE_KEY, json.dumps(message))
                logger.info('发送 Source 更新消息成功, 接收者 {} 个'.format(recv_cnt))

            self.result_parsers = []

            for source_item in self.origin_source_list:
                source = Source(source_item)
                if source.source_enable:
                    self.result_parsers.append(ResultParser(source))
            logger.info('重新加载配置文件完成, 总计 {} 个来源'.format(len(self.result_parsers)))

            return True
        except Exception as e:
            logger.error('保存资源失败, {}'.format(e))
            return False

    def verify_source(self, source_json: dict):
        """
        验证资源
        :param source_json:
        :return:
        """

        source_keys = []
        for key in SourceKeys.__dict__:
            if key.startswith('__'):
                continue
            source_keys.append(SourceKeys.__dict__[key])

        # 可以为空的字段
        EXCLUDE_KEYS = [SourceKeys.REQUEST_HEADER, SourceKeys.SEARCH_HEADER, SourceKeys.SEARCH_PARAMS,
                        SourceKeys.SEARCH_VERIFY, SourceKeys.SEARCH_VERIFY_URL, SourceKeys.SEARCH_VERIFY_SUBMIT_URL,
                        SourceKeys.DETAIL_PAGE_EPISODE_LIST, SourceKeys.SEARCH_RESULT_ITEM_RATING,
                        SourceKeys.SEARCH_RESULT_ITEM_STATUS]
        for key in source_keys:
            # 检查必须字段
            if key not in source_json and key not in EXCLUDE_KEYS:
                message = '缺少 {} 字段'.format(key)
                logger.warn('资源 {} 缺少 {} 字段'.format(source_json['sourceId'], key))
                return message
            elif key in source_json and key not in EXCLUDE_KEYS:
                value = source_json[key]
                if value is None or value == '':
                    message = '字段 {} 不能为空'.format(key)
                    logger.warn('资源 {} 字段 {} 不能为空'.format(source_json['sourceId'], key))
                    return message

        # 检查字段格式
        if str(source_json[SourceKeys.SOURCE_ENABLE]).lower() not in ['true', 'false'] or \
                str(source_json[SourceKeys.SEARCH_VERIFY]).lower() not in ['true', 'false']:
            message = '字段 {} 格式错误，应该是true/false'.format(SourceKeys.SOURCE_ENABLE)
            logger.warn('资源 {} 字段 {} 字段格式错误，应该是true/false'.format(source_json['sourceId'], SourceKeys.SOURCE_ENABLE))
            return message

        if not str(source_json[SourceKeys.SOURCE_PRIORITY]).isdigit():
            message = '字段 {} 格式错误，应该是数字'.format(SourceKeys.SOURCE_PRIORITY)
            logger.warn('资源 {} 字段 {} 字段格式错误，应该是数字'.format(source_json['sourceId'], SourceKeys.SOURCE_PRIORITY))
            return message

        if str(source_json[SourceKeys.REQUEST_METHOD]).lower() not in ['get', 'post'] or \
                str(source_json[SourceKeys.SEARCH_METHOD]).lower() not in ['get', 'post']:
            message = '字段 {} 格式错误，应该是get/post'.format(SourceKeys.REQUEST_METHOD)
            logger.warn('资源 {} 字段 {} 字段格式错误，应该是get/post'.format(source_json['sourceId'], SourceKeys.REQUEST_METHOD))
            return message

        if str(source_json[SourceKeys.REQUEST_CHARSET]).lower() not in ['utf-8', 'gbk', 'gb2312'] or \
                str(source_json[SourceKeys.RESPONSE_CHARSET]).lower() not in ['utf-8', 'gbk', 'gb2312']:
            message = '字段 {} 格式错误，应该是utf-8/gbk/gb2312'.format(SourceKeys.REQUEST_CHARSET)
            logger.warn(
                '资源 {} 字段 {} 字段格式错误，应该是utf-8/gbk/gb2312'.format(source_json['sourceId'], SourceKeys.REQUEST_CHARSET))
            return message

        if not is_valid_json(source_json[SourceKeys.REQUEST_HEADER]) or \
                not is_valid_json(source_json[SourceKeys.SEARCH_HEADER]):
            message = '字段 {} 格式错误，应该是json/obj格式'.format(SourceKeys.REQUEST_HEADER)
            logger.warn('资源 {} 字段 {} 字段格式错误，应该是json/obj格式'.format(source_json['sourceId'], SourceKeys.REQUEST_HEADER))
            return message

        if str(source_json[SourceKeys.SEARCH_METHOD]).lower() == 'post' and \
                ('&' not in str(source_json[SourceKeys.SEARCH_PARAMS]) or
                 '=' not in str(source_json[SourceKeys.SEARCH_PARAMS])):
            message = '字段 {} 格式错误，应该要包含&，=符号'.format(SourceKeys.SEARCH_PARAMS)
            logger.warn('资源 {} 字段 {} 字段格式错误，应该要包含&，=符号'.format(source_json['sourceId'], SourceKeys.SEARCH_PARAMS))
            return message

        if '{keyword}' not in str(source_json[SourceKeys.SEARCH_URL]) or \
                (str(source_json[SourceKeys.SEARCH_METHOD]).lower() == 'post' and
                 '{keyword}' not in str(source_json[SourceKeys.SEARCH_PARAMS])):
            message = '字段 {} 格式错误，应该要包含 {}'.format(SourceKeys.SEARCH_URL, "{keyword}")
            logger.warn(
                '资源 {} 字段 {} 字段格式错误，应该要包含 {}'.format(source_json['sourceId'], SourceKeys.SEARCH_URL, "{keyword}"))
            return message

        logger.info('资源 {} 校验通过'.format(source_json['sourceId']))
        return True

    def test_search(self, source_json: any, keyword: str):
        """
        测试搜索
        :param keyword:
        :return:
        """
        if type(source_json) == str:
            source_json = json.loads(source_json)

        source = Source(source_json)
        result_parser = ResultParser(source)
        return self._search(result_parser, keyword, False)

    def test_detail(self, source_json: dict, url: str):
        """
        测试详情
        :param url:
        :return:
        """
        source = Source(source_json)
        return self._detail(source, url, False)

    def test_play(self, source_json: dict, url: str):
        """
        测试播放
        :param source_json: 数据源
        :param url: 地址
        :return:
        """
        source = Source(source_json)
        return self._play(source, url, False)

    def _load_source(self):
        config_list = []
        if RUN_ROLE == 'master':
            logger.info('加载配置文件 {}'.format(self.path))
            with open(self.path, 'r') as f:
                config_list = json.load(f)
            Redis.set(SOURCE_KEY, parse_value(config_list))
            logger.info('已经将 Source 设置到 Redis')
        elif RUN_ROLE == 'slave':
            temp_source = Redis.get(SOURCE_KEY)
            if temp_source:
                config_list = json.loads(temp_source)
                logger.info('从 REDIS 加载 Source 文件 {}'.format(self.path))
        result_parsers = []
        for config_item in config_list:
            self.origin_source_list.append(config_item)
            source = Source(config_item)
            self.origin_source_map[source.source_id] = config_item
            if source.source_enable:
                result_parsers.append(ResultParser(source))
        logger.info('加载配置文件完成, 总计 {} 个来源'.format(len(result_parsers)))

        # 注册消息队列
        message_sub = Redis.pubsub()
        message_sub.subscribe(**{MESSAGE_KEY: self._on_message})
        message_sub.run_in_thread(sleep_time=0.1, daemon=True)

        logger.info('注册 Source 更新消息队列成功 {}'.format(MESSAGE_KEY))

        return result_parsers

    def _on_message(self, message: dict):
        """
        消息队列回调
        :param message: 消息
        :return:
        """

        # message = message.decode()

        content = message['data'].decode()
        content = json.loads(content)
        logger.info('收到消息队列消息 {}'.format(content))
        message_id = content['message_id']
        message_content = content['message_content']
        message_from = content['message_from']

        if message_from == SERVER_NAME:
            logger.info('消息来自相同机器 {}，跳过'.format(message_content))
            return

        message_key = parse_key('MSG', message_id, message_from)
        lock_result = Redis.setnx(message_key, message_content)

        if not lock_result:
            logger.info('消息 {} 已经处理过'.format(message_key))
            return

        logger.info('消息队列消息 {} 成功设置锁'.format(message_key))
        Redis.expire(message_key, 30)

        if message_content == 'source_update':
            logger.info('收到 Source 更新消息')
            cache_source_list = Redis.get(SOURCE_KEY)
            if cache_source_list:
                cache_source_list = json.loads(cache_source_list)

                if RUN_ROLE == 'master':
                    with open(self.path, 'w') as f:
                        json.dump(cache_source_list, f, indent=4, ensure_ascii=False)
                    logger.info('更新本地资源成功')

                self.result_parsers = []

                for source_item in cache_source_list:
                    self.origin_source_list.append(source_item)
                    source = Source(source_item)
                    self.origin_source_map[source.source_id] = source_item
                    if source.source_enable:
                        self.result_parsers.append(ResultParser(source))
                logger.info('重新加载配置文件完成, 总计 {} 个来源'.format(len(self.result_parsers)))
            logger.info('Source 更新成功')

    def search(self, keyword: str, refresh: bool = False):
        """
        解析搜索
        :param keyword: 关键字
        :param refresh: 是否刷新缓存
        :return:
        """
        startTime = time.time()
        results = []
        for result in self.thread_pool.map(lambda parser: self._search(parser, keyword, refresh=refresh),
                                           self.result_parsers):
            results.append(result)
        endTime = time.time()
        logger.info('解析搜索结果耗时：{}'.format(endTime - startTime))
        return results

    def detail(self, source_id: str, detail_url: str, refresh: bool = False):
        """
        解析详情
        :param detail_url: 详情链接
        :param source_id: 资源id
        :param refresh: 是否刷新缓存
        :return:
        """
        # 检查资源是否存在
        if source_id not in self.origin_source_map:
            return None
        source = Source(self.origin_source_map[source_id])
        return self._detail(source, detail_url, refresh=refresh)

    def play(self, source_id: str, play_url: str, refresh: bool = False):
        """
        解析播放
        :param play_url: 播放链接
        :param source_id: 资源id
        :param refresh: 是否刷新缓存
        :return:
        """
        # 检查资源是否存在
        if source_id not in self.origin_source_map:
            return None
        source = Source(self.origin_source_map[source_id])
        return self._play(source, play_url, refresh=refresh)

    def _search(self, result_parser: ResultParser, keyword: str, use_cache: bool = True, refresh: bool = False):
        """
        解析搜索 用于线程搜索
        :param result_parser: 解析器
        :param keyword: 关键字
        :return:
        """
        try:

            cache_key = parse_key('search', result_parser.id, keyword)

            # 刷新缓存，直接删除缓存
            if refresh:
                logger.info('刷新缓存，删除缓存 {}'.format(cache_key))
                Redis.delete(cache_key)

            # 判断是否使用缓存
            if use_cache and not refresh:
                cache_result = Redis.get(cache_key)
                if cache_result:
                    logger.info('使用缓存 {}'.format(cache_key))
                    return json.loads(cache_result)

            result = {
                'id': result_parser.id,
                'name': result_parser.name,
                'result': result_parser.parse(keyword)
            }

            if use_cache and 'result' in result and result['result']:
                logger.info('解析搜索结果已缓存 {}'.format(cache_key))
                Redis.set(cache_key, parse_value(result), ex=60 * 20)

            return result
        except Exception as e:
            logger.error('解析 [{}] 搜索出错：{}'.format(result_parser.id, e))
        return {
            'id': result_parser.id,
            'name': result_parser.name,
            'result': []
        }

    def _detail(self, source: Source, detail_url: str, use_cache: bool = True, refresh: bool = False):
        """
        解析详情
        :param detail_url: 详情链接
        :return:
        """
        source_id = source.source_id
        # 检查自由是否使能
        if not source.source_enable:
            logger.error('资源 [{}] 未启用'.format(source_id))
            return None

        # 检查详情链接是否合法
        source_host = parse_url(source.source_home_page).netloc
        detail_host = parse_url(detail_url).netloc

        if source_host != detail_host:
            logger.error('资源 [{}] 与链接不匹配'.format(source_id))
            return None

        detail_parser = DetailParser(source)

        cache_key = parse_key('detail', source_id, detail_url)

        # 刷新缓存，直接删除缓存
        if refresh:
            logger.info('刷新缓存，删除缓存 {}'.format(cache_key))
            Redis.delete(cache_key)

        # 判断是否使用缓存
        if use_cache and not refresh:
            cache_result = Redis.get(cache_key)
            if cache_result:
                logger.info('使用缓存 {}'.format(cache_key))
                return json.loads(cache_result)

        result = detail_parser.parse(detail_url)

        if use_cache and 'lineList' in result and result['lineList']:
            logger.info('解析详情已经缓存 {}'.format(cache_key))
            Redis.set(cache_key, parse_value(result), ex=60 * 30)

        logger.info('资源 [{}] 解析详情结果：{}'.format(source_id, result))
        return result

    def _play(self, source: Source, play_url: str, use_cache: bool = True, refresh: bool = False):
        """

        :param source:
        :param play_url:
        :return:
        """
        source_id = source.source_id
        # 检查自由是否使能
        if not source.source_enable:
            logger.error('资源 [{}] 未启用'.format(source_id))
            return None

        # 检查详情链接是否合法
        source_host = parse_url(source.source_home_page).netloc
        detail_host = parse_url(play_url).netloc

        if source_host != detail_host:
            logger.error('资源 [{}] 与链接不匹配'.format(source_id))
            return None

        play_parser = PlayParser(source)

        cache_key = parse_key('play', source_id, play_url)

        # 刷新缓存，直接删除缓存
        if refresh:
            logger.info('刷新缓存，删除缓存 {}'.format(cache_key))
            Redis.delete(cache_key)

        # 判断是否使用缓存
        if use_cache and not refresh:
            cache_result = Redis.get(cache_key)
            if cache_result:
                logger.info('使用缓存 {}'.format(cache_key))
                return json.loads(cache_result)

        result = play_parser.parse(play_url)

        if use_cache and 'playerUrl' in result and result['playerUrl']:
            logger.info('解析播放地址已经缓存 {}'.format(cache_key))
            Redis.set(cache_key, parse_value(result), ex=60 * 40)

        logger.info('资源 [{}]，地址 {} 解析播放结果：{}'.format(source_id, play_url, result))
        return result
