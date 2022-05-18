#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/5/2 10:20
@Author   : colinxu
@File     : play_parser.py
@Desc     : 播放解析器
"""
import base64
import json
import random

from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse, urlunparse

from model.source import Source
from util.common import is_empty, is_valid_json
from util.http import http_post, http_get
from util.logging import Logger
from command.command_helper import CommandHelper
from constant.config import PLAYER_SERVERS, PLAYER_RULES, PLAYER_WEIGHTS, PROXY_RULES

logger = Logger(__name__).get_logger()

cmd_helper = CommandHelper()


class PlayParser(object):
    def __init__(self, source: Source):
        self.s = source

    def _request(self, url):
        method = self.s.request_method
        method = method.lower()
        header = self.s.request_header if not is_empty(self.s.request_header) else {}
        if method == 'post':
            return http_post(url, headers=header)
        else:
            return http_get(url, headers=header)

    def parse(self, play_url: str):
        """
        解析播放页面
        :param play_url: 播放地址
        :return: 解析结果
        """
        response = self._request(play_url)
        page = ''
        if response.status_code == 200:
            page = response.text
            page = page.encode(self.s.response_charset)

        soup = BeautifulSoup(page, 'lxml')
        base_tag = soup.select_one('html')

        title = cmd_helper.execute(base_tag, self.s.play_page_title)
        display_line_name = cmd_helper.execute(base_tag, self.s.play_page_line_name)
        line_config = cmd_helper.execute(base_tag, self.s.play_page_line_config)
        if is_valid_json(line_config):
            line_config = json.loads(line_config)
        play_line_name = line_config['from'] if line_config and 'from' in line_config else None
        if play_line_name == '' or play_line_name is None:
            play_line_name = display_line_name
        if is_empty(play_line_name):
            logger.info('播放页面解析失败，没有找到播放线路')
            return {
                'title': '',
                'lineName': '',
                'lineConfig': '',
                'playerUrl': ''
            }
        player_config_url = self.s.play_page_player_config_url.format(lineName=play_line_name)

        # FIXME 请求需要时间 需要优化
        player_url = self._get_play_url(player_config_url)

        encrypt_type = line_config['encrypt'] if 'encrypt' in line_config else 3
        line_url = line_config['url'] if 'url' in line_config else ''
        if encrypt_type == 1:
            line_url = unquote(line_url)
        elif encrypt_type == 2:
            line_url = base64.b64decode(line_url).decode('utf-8')
            line_url = unquote(line_url)
        else:
            pass

        is_official = False

        for official_host in PLAYER_RULES:
            if official_host in line_url:
                player_url = random.choices(PLAYER_SERVERS, weights=PLAYER_WEIGHTS, k=1)[0] + line_url
                is_official = True
                break

        if not is_official:
            # 直接是m3u8的地址 使用播放器替换
            if line_url.endswith('.m3u8') and player_url is None:
                player_url = random.choices(PLAYER_SERVERS, weights=PLAYER_WEIGHTS, k=1)[0] + line_url
            elif line_url.endswith('.m3u8') and player_url.endswith('.html') and self.s.source_id.lower() == 'libvio':
                player_url = '/proxy/libvio' + player_url + '?line=' + line_url
            else:
                # 使用自建代理替换
                player_url = (player_url if player_url else '') + line_url
                player_proxy = self.get_proxy_map()
                for proxy in player_proxy.keys():
                    if proxy in player_url:
                        player_url = player_url.replace(proxy, player_proxy[proxy])
                        break

        logger.info('解析播放页面成功，播放地址：{}'.format(player_url))

        # urlparse_result = urlparse(player_url)
        # query = '{}={}&{}'.format('referer', self.s.source_home_page, urlparse_result.query)
        # player_url = urlparse_result.scheme + '://' + urlparse_result.netloc + urlparse_result.path + '?' + query
        # logger.info(query)

        return {
            'title': title,
            'lineName': display_line_name,
            'lineConfig': line_config,
            'playerUrl': player_url
        }

    def _get_play_url(self, play_config_url: str):
        """
        获取播放地址
        :param play_url:播放地址
        :return:
        """
        try:
            response = self._request(play_config_url)
            if response.status_code == 200:
                page = response.text
                page = page.encode(self.s.response_charset)
                soup = BeautifulSoup(page, 'lxml')
                base_tag = soup.select_one('html')
                play_url = cmd_helper.execute(base_tag, self.s.play_page_player_url)
                return play_url
            else:
                return None
        except Exception as e:
            logger.error('获取播放地址失败，{}'.format(e))
            return None

    def get_proxy_map(self):
        """
        获取代理服务器
        :return:
        """
        result = {}
        for key, value in PROXY_RULES.items():
            proxy_key = value['host']
            proxy_value = ''
            proxy_value = proxy_value + '/proxy/' + key
            result[proxy_key] = proxy_value
        return result
