#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/5/20 22:22
@Author   : colinxu
@File     : player.py
@Desc     : 播放器
"""
from .command_helper import CommandHelper
from .http import http_get
from bs4 import BeautifulSoup

command_helper = CommandHelper()


class Player:
    def __init__(self, play_url, config):
        self.play_url = play_url
        self.config = config
        self.html_soup = None
        self._request()

    def _request(self):
        header = {}
        response = http_get(self.play_url, headers=header)
        if response.status_code == 200:
            self.html_soup = BeautifulSoup(response.text, 'lxml').select_one('html')

    def get_site_info(self):
        pattern = self.config['siteInfo']
        return command_helper.execute(self.html_soup, pattern)

    def get_player_config(self):
        pattern = self.config['playerConfig']
        return command_helper.execute(self.html_soup, pattern)
