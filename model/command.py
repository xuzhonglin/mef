#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/4/28 17:43
@Author   : colinxu
@File     : command.py
@Desc     : 指令模型
"""


class Command(object):

    def __init__(self, cmd: str, args):
        self.cmd = cmd
        self.args = args

    def __str__(self):
        return '{"cmd": "%s", "args": "%s"}' % (self.cmd, self.args)
