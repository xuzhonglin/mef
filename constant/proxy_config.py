#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/5/2 20:46
@Author   : colinxu
@File     : proxy_config.py
@Desc     : 代理配置
"""


class ProxyConfig(object):
    """
    代理配置
    """
    LOCAL_HOST = 'http://0.0.0.0:10282'
    # DOMAIN_HOST = ''
    # 代理服务器
    TARGET_MAP = {
        'dd520': {
            'host': 'https://bo.dd520.cc',
            'headers': {
                'Referer': 'https://www.libvio.com'
            },
            'replacements': []
        },
        'libvio1': {
            'host': 'https://sh-data-s01.chinaeast2.cloudapp.chinacloudapi.cn',
            'headers': {
                'Referer': 'https://www.libvio.com'
            },
            'replacements': []
        },
        'libvio2': {
            'host': 'https://cbsh-d0145678.chinaeast2.cloudapp.chinacloudapi.cn',
            'headers': {
                'Referer': 'https://www.libvio.com'
            },
            'replacements': [
                ['/Content', '/proxy/libvio2/Content'],
                ['/Scripts', '/proxy/libvio2/Scripts'],
                ['/ParsePlayer', '/proxy/libvio2/ParsePlayer'],
            ]
        },
        '555dy1': {
            'host': 'https://zyz.021huaying.com',
            'headers': {
                'Referer': 'https://www.5dy5.cc'
            },
            'replacements': [
                # ['./js/play.js', 'https://zyz.021huaying.com/duoduo/js/play.js']
            ]
        },
        'image': {
            'host': '*',
            'headers': {},
            'replacements': []
        }
    }

    def get_proxy_map(self):
        """
        获取代理服务器
        :return:
        """
        result = {}
        for key, value in self.TARGET_MAP.items():
            # proxy_key = value['host'].split('//')[1]
            proxy_key = value['host']
            # proxy_value = self.LOCAL_HOST if DOMAIN_NAME == '' else DOMAIN_NAME
            proxy_value = ''
            proxy_value = proxy_value + '/proxy/' + key
            result[proxy_key] = proxy_value
        return result
