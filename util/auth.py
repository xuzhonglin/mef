#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/5/16 20:54
@Author   : colinxu
@File     : auth.py
@Desc     : 授权验证
"""
import base64
import hmac
import time
import json
import copy
from pyotp import TOTP
from constant.config import ADMIN_SECRET, ADMIN_USERNAME, ADMIN_PASSWORD
from util.redis import get_redis, parse_key

Redis = get_redis()


class Jwt(object):

    @staticmethod  # 静态方法的装饰器封装一下  专门负责做计算用的函数
    def encode(self_payload, key, exp=300):
        # self_payload  含有私有声明的字典
        # key 自定的key
        # exp 过期时间

        # 生成header
        header = {'typ': 'JWT', 'alg': 'HS256'}
        # header_json = json.dumps(header)  # 这样转为json串不行，有空格，损耗带宽
        header_json = json.dumps(header, separators=(',', ':'), sort_keys=True)
        # 这样逗号冒号前后就没有空格了,sort_keys=True 使出来的json串变的有序了，在做hmac或其他哈希的计算的时候，串值一定是稳定的
        # separators分割符 第一个参数代表的是每个键值对之间用什么分割，第二个参数是每个键和值之间用什么分割
        # sort_keys 生成有序的json串
        header_json_base64 = Jwt.b64encode(header_json.encode())

        # init payload
        self_payload_copy = copy.deepcopy(self_payload)  # 为了不污染传进来的字典
        # 给拷贝出来的字典中加入公有声明
        self_payload_copy["exp"] = time.time() + exp  # 过期时间
        self_payload_copy_json = json.dumps(self_payload_copy, separators=(',', ':'), sort_keys=True)
        self_payload_copy_json_base64 = Jwt.b64encode(self_payload_copy_json.encode())

        # init sign
        hm = hmac.new(key.encode(), header_json_base64 + b'.' + self_payload_copy_json_base64,
                      digestmod="SHA256")  # 两个都是字节码所以连接符*点*也要是字节码
        hm_base64 = Jwt.b64encode(hm.digest())  # 取hm的二进制结果，然后进行base64的转码

        # jwt token 诞生  字节码
        return header_json_base64 + b'.' + self_payload_copy_json_base64 + b'.' + hm_base64

    @staticmethod
    def b64encode(js):  # 为了将base64转换修改为urlsafe
        return base64.urlsafe_b64encode(js).replace(b"=", b"")

    @staticmethod
    def b64decode(bs):
        # 加回来等号
        rem = len(bs) % 4  # 取余
        if rem > 0:
            bs += b'=' * (4 - rem)

        return base64.urlsafe_b64decode(bs)

    @staticmethod
    def decode(token, key):
        # 传入jwt的值(令牌) 和只有调用者知道的key

        # 校验签名
        header_bs, payload_bs, signature_bs = token.split(b".")  # 因为是字节串
        # header_bs, payload_bs, signature_bs = token.split(".")  # 因为是字节串
        hm = hmac.new(key.encode(), header_bs + b"." + payload_bs, digestmod="SHA256")
        if signature_bs != Jwt.b64encode(hm.digest()):  # 将签名结果和传过来的sign进行对比
            raise

        # 校验时间
        payload_js = Jwt.b64decode(payload_bs)  # 解码为json
        payload = json.loads(payload_js)  # 解码为字典

        now = time.time()  # 当前时间
        if int(now) > int(payload["exp"]):  # 登录时间过期
            raise
        return payload


def totp_validate(totp_code: str):
    """
    验证totp
    :param totp_code: totp验证码
    :return:
    """
    totp = TOTP(ADMIN_SECRET)
    return totp.verify(totp_code, valid_window=1)


def auth_login(username: str, password: str, totp_code: str):
    try:
        cache_key = parse_key('login', username)
        failed_cnt = Redis.get(cache_key)
        if failed_cnt and int(failed_cnt) >= 6:
            return '失败次数过多，请30分钟后重试', False

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD and totp_validate(totp_code):
            return gen_jwt(username), True

        Redis.incrby(cache_key, 1)
        if failed_cnt is None:
            Redis.expire(cache_key, 60 * 30)
    except Exception as e:
        print(e)
    return '用户名或密码错误、动态码错误', False


def gen_jwt(username: str, expire: int = 60 * 60 * 6):
    payload = {
        'exp': time.time() + expire,  # EXpiration Time 此token的过期时间的时间戳 time.time()+300s  给一个未来过期时间
        'iss': 'Mef-Authority',  # (issuer) Claim 指明此token的签发者  是那台机器签发的token (当前项目没用)
        'aud': 'AdminLogin',  # (Audience) Claim 指明此token的签发群体 token签发面向群体是那些人 区分pc，ios，android  (当前项目没用)
        'iat': time.time(),  # (ISSued At) Claim 指明此创建时间的时间戳
        # 以上四项是我们的公有声明 保留字
        # 下边私有声明
        'username': username
    }
    return Jwt.encode(payload, ADMIN_SECRET, expire).decode()


def auth_jwt(jwt_str: str):
    try:
        Jwt.decode(jwt_str.encode(), ADMIN_SECRET)
        return True
    except Exception as e:
        print(e)
        return False
