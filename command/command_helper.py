#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/4/28 17:38
@Author   : colinxu
@File     : helper.py
@Desc     : 命令解析
"""
from model.command import Command
from command.functions import Functions as func
from util.logging import Logger

logger = Logger('CommandHelper').get_logger()


class CommandHelper(object):

    def __init__(self):
        pass

    def execute(self, source: object, pattern: str):
        """
        执行命令
        :param source: 源数据
        :param pattern: 指令
        :return: 结果
        """
        logger.debug("执行命令：{}".format(pattern))
        command_array = self._parse_command(pattern)
        return self._execute_command(source, command_array)

    def _parse_command(self, pattern: str):
        """
        解析选择器
        :param pattern:自定义选择器
        :return: 命令列表
        """
        if pattern is None or pattern == "":
            logger.error("自定义选择器有误 {}".format(pattern))
            return None

        extent_func = None

        # 包含额外的函数
        if "$" in pattern:
            logger.debug("检测到包含额外的函数")
            pattern, extent_func = pattern.split("$")[0], pattern.split("$")[1]

        # 分离选择器和属性
        if "@" in pattern:
            selector = pattern.split("@")[0].strip()
            attribute = pattern.split("@")[1].strip()
        else:
            selector = pattern.strip()
            attribute = None

        command_array = []

        # 分离每个选择器
        selector_array = selector.split('>')
        for sub_selector in selector_array:
            sub_selector = sub_selector.strip()
            if sub_selector == "":
                continue
            sub_selector_prefix = sub_selector[0]
            # 如果是类选择器 则添加类选择器前缀
            if ' ' in sub_selector and sub_selector_prefix in ['.']:
                sub_selector = sub_selector.replace(' ', sub_selector_prefix)
            if '|' in sub_selector:
                result_index = int(sub_selector.split('|')[-1].strip())
                sub_selector = sub_selector.split('|')[0].strip()
                command = [Command('select', sub_selector), Command('index', result_index)]
                command_array.extend(command)
            else:
                command = [Command('select', sub_selector), Command('index', -1)]
                command_array.extend(command)

        if attribute is not None:
            command_array.append(Command('attr', attribute))

        # 如果有额外的函数
        if extent_func is not None:
            func_array = extent_func.split(';')
            for func_item in func_array:
                func_item = func_item.strip()
                if func == "":
                    continue
                func_name, func_args = func_item.split(':')[0].strip(), func_item.split(':')[1].strip()
                func_args = func_args.split(',')
                command_array.append(Command(func_name, tuple(func_args)))

        return command_array

    def _execute_command(self, source: object, command_array: list):
        """
        执行命令
        :param source: 源数据
        :param command_array: 指令列表
        :return: 执行结果
        """

        if command_array is None or len(command_array) == 0:
            logger.info("命令列表为空")
            return None

        func_name = command_array[0].cmd
        func_args = command_array[0].args
        logger.debug("执行指令 CMD：{} ARGS：{}".format(func_name, func_args))
        ret = getattr(func, func_name)(func, source, func_args)
        # logger.debug("执行结果：{}".format(ret))
        # 如果没有下一个命令
        if len(command_array) == 1:
            return ret
        return self._execute_command(ret, command_array[1:])
