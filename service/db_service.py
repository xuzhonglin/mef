#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/5/8 12:20
@Author   : colinxu
@File     : db_service.py
@Desc     : 
"""
import sqlite3

from constant.config import DB_PATH
from util.logging import Logger

logger = Logger(__name__).get_logger()


class DbService:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

    def _get_table_all(self, table_name):
        sql = "select * from %s" % table_name
        self.cursor.execute(sql)

    def _insert(self, table_name, data):
        sql = "insert into %s values %s" % (table_name, data)
