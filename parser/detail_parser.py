#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/4/27 17:49
@Author   : colinxu
@File     : detail_parser.py
@Desc     : 详情解析器
"""
from bs4 import BeautifulSoup

from model.source import Source
from util.http import http_get, http_post
from util.common import complete_url, is_empty
from command.command_helper import CommandHelper
from constant.config import LINE_EXCLUDE_RULES

cmd_helper = CommandHelper()


class DetailParser:
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

    def parse(self, url: str):
        """
        解析详情页
        :param url: 详情页地址
        :return: 返回解析后的数据
        """
        response = self._request(url)
        page = ''
        if response.status_code == 200:
            page = response.text
            page = page.encode(self.s.response_charset)

        soup = BeautifulSoup(page, 'lxml')
        base_tag = soup.select_one('body')

        title = cmd_helper.execute(base_tag, self.s.detail_page_title)

        image = cmd_helper.execute(base_tag, self.s.detail_page_image)
        description = cmd_helper.execute(base_tag, self.s.detail_page_description)

        line_tags = cmd_helper.execute(base_tag, self.s.detail_page_line_list)

        # 剧集是否在线路子元素下
        episode_list_selector = self.s.detail_page_episode_list
        is_episode_under_line = episode_list_selector is None or len(episode_list_selector) == 0

        line_list = {}

        if not line_tags or len(line_tags) == 0:
            return {
                'title': title,
                'image': image,
                'description': description,
                'lineNames': [],
                'lineList': []
            }

        for line_tag in line_tags:
            line_name = cmd_helper.execute(line_tag, self.s.detail_page_line_name)
            # 剔除不需要的线路
            if line_name is None or self._is_exclude(line_name, LINE_EXCLUDE_RULES):
                continue
            line_name = line_name.strip()
            if line_name not in line_list:
                line_list[line_name] = []

            # 剧集是在线路元素下
            if is_episode_under_line:
                episode_tags = cmd_helper.execute(line_tag, self.s.detail_page_episode_item)
                for episode_tag in episode_tags:
                    episode_title = cmd_helper.execute(episode_tag, self.s.detail_page_episode_item_title)
                    episode_url = cmd_helper.execute(episode_tag, self.s.detail_page_episode_item_url)
                    episode_url = complete_url(self.s.source_home_page, episode_url)
                    line_list[line_name].append({
                        'title': episode_title,
                        'url': episode_url
                    })

        # 剧集不在线路元素下
        if not is_episode_under_line:
            episode_list_tags = cmd_helper.execute(base_tag, self.s.detail_page_episode_list)

            for index, episode_list_tag in enumerate(episode_list_tags):
                # 超出线路直接跳出
                if index + 1 > len(line_list):
                    break
                episode_tags = cmd_helper.execute(episode_list_tag, self.s.detail_page_episode_item)
                line_name = list(line_list.keys())[index]
                for episode_tag in episode_tags:
                    episode_title = cmd_helper.execute(episode_tag, self.s.detail_page_episode_item_title)
                    episode_url = cmd_helper.execute(episode_tag, self.s.detail_page_episode_item_url)
                    episode_url = complete_url(self.s.source_home_page, episode_url)
                    line_list[line_name].append({
                        'title': episode_title,
                        'url': episode_url
                    })

        return {
            'title': title,
            'image': image,
            'description': description,
            'lineNames': [line_name for line_name in line_list.keys()],
            'lineList': line_list
        }

    def _is_exclude(self, target, exclude_list):
        for exclude in exclude_list:
            if exclude in target:
                return True
        return False
