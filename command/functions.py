#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/4/28 20:54
@Author   : colinxu
@File     : functions.py
@Desc     : 函数
"""
from bs4.element import Tag, ResultSet


class Functions(object):

    def __init__(self):
        pass

    def select(self, tag: Tag, selector: str):
        """
        执行选择器
        :param tag: 标签
        :param selector: css选择器
        :return:
        """
        if tag is None or len(tag) == 0 or selector is None:
            return None
        if isinstance(tag, ResultSet):
            tag = tag[0]
        return tag.select(selector)

    def attr(self, tag: Tag, attr: str):
        """
        获取标签的属性
        :param tag: 标签
        :param attr: 属性名
        :return:
        """
        if tag is None or len(tag) == 0 or attr is None or attr.split() == '':
            return None
        if isinstance(tag, ResultSet):
            tag = tag[0]
        if attr == 'text':
            return tag.text.strip()
        return tag.get(attr).strip() if attr in tag.attrs else None

    def index(self, data: list, position: int):
        """
        获取列表中的指定位置的元素
        :param data: 数据列表
        :param position: 位置
        :return:
        """
        if data is None or len(data) - 0 < position < -1:
            return None
        return data[position] if position >= 0 else data

    def replace(self, data: str, args):
        """
        替换字符串
        :param data: 被替换字符串
        :param args: 替换参数(old, new)
        :return:
        """
        if data is None or args is None or len(args) != 2:
            return None
        old, new = args
        if new == 'null' or new == 'None':
            new = ''

        if new == 'blank':
            new = ' '

        return data.replace(old, new)

    def substr(self, data: str, args):
        """
        截取字符串
        :param data: 被截取字符串
        :param args: 参数(start, end)
        :return:
        """
        if data is None or args is None or len(args) != 2:
            return None
        start, end = args
        if not start.isdigit() or not end.isdigit():
            return None
        start, end = int(start), int(end)
        if start < 0 or end < 0 or start > end:
            return None
        return data[start:end]

    def split(self, data: str, args):
        """
        分割字符串
        :param data: 被分割字符串
        :param args: 分割参数(sep, start [, end])
        :return:
        """
        if data is None or args is None:
            return None

        if len(args) == 2:
            sep, start_index = args
            end_index = start_index
        elif len(args) == 3:
            sep, start_index, end_index = args
        else:
            return None

        if not start_index.isdigit() or not end_index.isdigit():
            return None
        start_index, end_index = int(start_index), int(end_index)

        if start_index < 0 or end_index < 0 or start_index > end_index:
            return None

        split_result = data.split(sep)
        if start_index == end_index:
            return split_result[start_index]
        return split_result[start_index:end_index]

    def strip(self, data: str):
        """
        去除字符串前后空格
        :param data: 被去除字符串
        :return:
        """
        if data is None:
            return None
        return data.strip()

    def insert(self, data: str, args):
        """
        插入字符串
        :param data: 被插入字符串
        :param args: 插入参数(index, string)
        :return:
        """
        if data is None or args is None:
            return None
        index, string = args
        if not index.isdigit():
            return None
        index = int(index)
        if index < 0:
            return None
        return data[:index] + string + data[index:]

    def join(self, data: list, args):
        """
        将列表中的元素拼接成字符串
        :param data: 列表
        :param args: 参数(sep)
        :return:
        """
        if data is None or args is None:
            return None
        sep = args
        return sep.join(data)

    def format(self, data: str, *args):
        """
        格式化字符串
        :param data: 被格式化字符串
        :param args: 格式化参数
        :return:
        """
        if data is None:
            return None
        return data.format(*args)
