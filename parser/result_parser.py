#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/4/27 16:51
@Author   : colinxu
@File     : parser.py
@Desc     : 结果解析器
"""

from bs4 import BeautifulSoup

from model.source import Source
from util.http import http_get, http_post
from util.common import complete_url, is_empty
from util.logging import Logger
from util.verify import Verify
from command.command_helper import CommandHelper
from constant.config import OCR_MAX_RETRY
from util.redis import get_redis, parse_key, parse_value

cmd_helper = CommandHelper()

logger = Logger(__name__).logger
code_verify = Verify()
Redis = get_redis()


class ResultParser:
    def __init__(self, source: Source):
        self.s = source
        self.id = source.source_id
        self.name = source.source_name
        self.cookie = ''

    def parse(self, keyword: str):
        """
        解析结果
        :param keyword: 关键字
        :return: 解析结果
        """
        response = self._search(keyword)
        page = ''
        if response.status_code == 200:
            page = response.text
            page = page.encode(self.s.response_charset)
        soup = BeautifulSoup(page, 'lxml')
        base_tag = soup.select_one('body')
        result_tag_list = cmd_helper.execute(base_tag, self.s.search_result_list)
        result_list = []

        # 可能开启了验证
        if result_tag_list is None:
            # TODO: 验证
            return result_list

        for result_tag in result_tag_list:
            title = cmd_helper.execute(result_tag, self.s.search_result_item_title)
            url = cmd_helper.execute(result_tag, self.s.search_result_item_url)
            image = cmd_helper.execute(result_tag, self.s.search_result_item_image)
            status = cmd_helper.execute(result_tag, self.s.search_result_item_status)
            rating = cmd_helper.execute(result_tag, self.s.search_result_item_rating)

            url = complete_url(self.s.source_home_page, url)
            image = complete_url(self.s.source_home_page, image)

            result_list.append({
                'title': title,
                'url': url,
                'image': image,
                'status': status,
                'rating': rating
            })
        return result_list

    def _search(self, keyword: str):
        """
        搜索
        :param keyword: 关键字
        :return:
        """
        url = self.s.search_url
        method = self.s.search_method
        method = method.lower()
        header = self.s.search_header if not is_empty(self.s.search_header) else {}
        if self.s.search_verify and is_empty(self.cookie):
            cache_key = parse_key('COOKIE', self.id)
            cache_result = Redis.get(cache_key)
            if cache_result:
                cache_result = cache_result.decode('utf-8')
                logger.info('[{}] 获取到cookie: {}'.format(self.id, cache_result))
                self.cookie = cache_result
            else:
                self.cookie = self._pre_verify_request()
            header['Cookie'] = header['Cookie'] if 'Cookie' in header else '' + ';' + self.cookie
        if method == 'post':
            params = self.s.search_params
            params.format(keyword=keyword)
            return http_post(url, data=params, headers=header)
        else:
            url = url.format(keyword=keyword)
            return http_get(url, headers=header)

    def _pre_verify_request(self, try_index=0):
        """
        预请求验证码
        :return:
        """
        try:
            if try_index >= OCR_MAX_RETRY:
                logger.error('验证码请求失败，已经超过最大请求次数，退出')
                return ''
            header = self.s.search_header if not is_empty(self.s.search_header) else {}
            response = http_get(self.s.search_verify_url, headers=header)
            if response.status_code == 200:
                code = code_verify.verify_code(image_bytes=response.content)
                header['Cookie'] = header['Cookie'] if 'Cookie' in header else '' + ';' + response.headers['Set-Cookie']
                response = http_get(self.s.search_verify_submit_url.format(verifyCode=code), headers=header)
                if response.status_code == 200:
                    logger.info('验证码验证成功，{}'.format(response.text))
                    self.cookie = header['Cookie']
                    self.cookie = self._format_cookie(self.cookie)
                    cache_key = parse_key('COOKIE', self.id)
                    Redis.set(cache_key, parse_value(self.cookie), 60 * 60 * 2)
                    logger.info('验证码验证成功，已经缓存到Redis，{}'.format(cache_key))
                else:
                    logger.info('验证码验证失败，正在重试，{}'.format(response.status_code))
                    self._pre_verify_request(try_index + 1)
                return self.cookie
        except Exception as e:
            logger.error('预先请求cookie异常 {}'.format(e))
        return self.cookie

    def _format_cookie(self, cookie: str):
        """
        格式化cookie
        :return:
        """
        if is_empty(cookie):
            return ''
        cookie_list = cookie.split(';')
        result_list = []
        for cookie in cookie_list:
            if not is_empty(cookie) and cookie.find('path=/') == -1:
                result_list.append(cookie)
        return ';'.join(result_list)
