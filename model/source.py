#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/4/27 15:42
@Author   : colinxu
@File     : source_pattern.py
@Desc     : 资源模式实体类
"""

from constant.source_keys import SourceKeys


class Source:

    def __init__(self, data: dict):
        self.source_id = data.get(SourceKeys.SOURCE_ID, "")
        self.source_name = data.get(SourceKeys.SOURCE_NAME, "")
        self.source_enable = data.get(SourceKeys.SOURCE_ENABLE, False)
        self.source_priority = data.get(SourceKeys.SOURCE_PRIORITY, 999)
        self.source_home_page = data.get(SourceKeys.SOURCE_HOME_PAGE, "")
        self.source_type = data.get(SourceKeys.SOURCE_TYPE, "maccms")
        self.request_method = data.get(SourceKeys.REQUEST_METHOD, "")
        self.request_charset = data.get(SourceKeys.REQUEST_CHARSET, "")
        self.request_header = data.get(SourceKeys.REQUEST_HEADER, {})
        self.response_charset = data.get(SourceKeys.RESPONSE_CHARSET, "")
        self.search_url = data.get(SourceKeys.SEARCH_URL, "")
        self.search_method = data.get(SourceKeys.SEARCH_METHOD, "")
        self.search_header = data.get(SourceKeys.SEARCH_HEADER, {})
        self.search_params = data.get(SourceKeys.SEARCH_PARAMS, "")
        self.search_verify = data.get(SourceKeys.SEARCH_VERIFY, "")
        self.search_verify_url = data.get(SourceKeys.SEARCH_VERIFY_URL, "")
        self.search_verify_submit_url = data.get(SourceKeys.SEARCH_VERIFY_SUBMIT_URL, "")
        self.search_result_list = data.get(SourceKeys.SEARCH_RESULT_LIST, "")
        self.search_result_item_title = data.get(SourceKeys.SEARCH_RESULT_ITEM_TITLE, "")
        self.search_result_item_url = data.get(SourceKeys.SEARCH_RESULT_ITEM_URL, "")
        self.search_result_item_image = data.get(SourceKeys.SEARCH_RESULT_ITEM_IMAGE, "")
        self.search_result_item_status = data.get(SourceKeys.SEARCH_RESULT_ITEM_STATUS, "")
        self.search_result_item_rating = data.get(SourceKeys.SEARCH_RESULT_ITEM_RATING, "")
        self.detail_page_title = data.get(SourceKeys.DETAIL_PAGE_TITLE, "")
        self.detail_page_image = data.get(SourceKeys.DETAIL_PAGE_IMAGE, "")
        self.detail_page_description = data.get(SourceKeys.DETAIL_PAGE_DESCRIPTION, "")
        self.detail_page_line_list = data.get(SourceKeys.DETAIL_PAGE_LINE_LIST, "")
        self.detail_page_line_name = data.get(SourceKeys.DETAIL_PAGE_LINE_NAME, "")
        self.detail_page_episode_list = data.get(SourceKeys.DETAIL_PAGE_EPISODE_LIST, "")
        self.detail_page_episode_item = data.get(SourceKeys.DETAIL_PAGE_EPISODE_ITEM, "")
        self.detail_page_episode_item_title = data.get(SourceKeys.DETAIL_PAGE_EPISODE_ITEM_TITLE, "")
        self.detail_page_episode_item_url = data.get(SourceKeys.DETAIL_PAGE_EPISODE_ITEM_URL, "")
        self.play_page_title = data.get(SourceKeys.PLAY_PAGE_TITLE, "")
        self.play_page_player_config_url = data.get(SourceKeys.PLAY_PAGE_PLAYER_CONFIG_URL, "")
        self.play_page_player_url = data.get(SourceKeys.PLAY_PAGE_PLAYER_URL, "")
        self.play_page_line_name = data.get(SourceKeys.PLAY_PAGE_LINE_NAME, "")
        self.play_page_line_config = data.get(SourceKeys.PLAY_PAGE_LINE_CONFIG, "")
