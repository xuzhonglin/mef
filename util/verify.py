#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/5/3 11:01
@Author   : colinxu
@File     : verify.py
@Desc     : 验证码识别工具
"""
import random
import time

import requests

from util.logging import Logger
from constant.config import OCR_ENABLED, OCR_SERVERS

logger = Logger(__name__).get_logger()


class Verify(object):
    def __init__(self):
        pass

    def verify_code(self, image_path: str = None, image_url: str = None, image_base64: str = None,
                    image_bytes: bytes = None):
        """
        验证码识别
        :param image_path: 图片路径
        :param image_url: 图片地址
        :param image_base64: 图片的base64
        :param image_bytes: 图片的bytes
        :return:
        """
        start_time = time.time()
        logger.info("验证码识别开始")
        _image_bytes = bytes()
        _image_base64 = str()
        if image_path:
            with open(image_path, 'rb') as f:
                _image_bytes = f.read()
        if image_url:
            resp = requests.get(image_url)
            _image_bytes = resp.content
        if image_base64:
            _image_base64 = image_base64
        if image_bytes:
            _image_bytes = image_bytes

        result = ''
        if _image_bytes:
            if OCR_ENABLED:
                ocr_server = random.choice(OCR_SERVERS)
                url = ocr_server + '/ocr/file/text'
                resp = requests.post(url, files={'image': _image_bytes})
                result = resp.text
        elif _image_base64:
            if OCR_ENABLED:
                ocr_server = random.choice(OCR_SERVERS)
                url = ocr_server + '/ocr/b64/text'
                resp = requests.post(url, data=_image_base64)
                result = resp.text
        logger.info("验证码识别结束，结果：{}， 耗时：{}".format(result, time.time() - start_time))
        return result
