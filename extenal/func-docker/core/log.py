#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/4/29 10:34
@Author   : colinxu
@File     : logging.py
@Desc     : 日志模块
"""

import logging
import logging.handlers
import os
import time

LOG_PATH = os.environ.get('PROXY_LOG_PATH', './logs')
LOG_LEVEL = os.environ.get('PROXY_LOG_LEVEL', 'INFO')
LOG_FILE_ENABLED = os.environ.get('PROXY_LOG_FILE_ENABLED', 'True') == 'True'


class Logger(object):
    """
    日志模块
    """

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(LOG_LEVEL)
        # self.formatter = logging.Formatter(
        #     '%(asctime)s %(levelname)s\t %(threadName)s\t- %(filename)s:%(lineno)d [%(funcName)s\t] : %(message)s')
        self.formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)7s - %(threadName)10s - %(module)15s.%(funcName)15s : %(message)s')

        # 控制台日志
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVEL)
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

        # 文件日志

        if LOG_FILE_ENABLED:

            if not os.path.exists(LOG_PATH) and not os.path.isdir(LOG_PATH):
                os.mkdir(LOG_PATH)

            log_file_name = 'mef-%s.log' % (self._today_data())
            log_file_path = os.path.join(LOG_PATH, log_file_name)
            file_handler = logging.handlers.TimedRotatingFileHandler(log_file_path, when='D', interval=1, backupCount=7)
            file_handler.setLevel(LOG_LEVEL)
            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)

    def get_handler(self):
        return self.logger.handlers

    def _today_data(self):
        return time.strftime("%Y-%m-%d", time.localtime())

    def get_logger(self):
        return self.logger
