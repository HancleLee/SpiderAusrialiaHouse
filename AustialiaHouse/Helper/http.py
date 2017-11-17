# -*- coding: utf-8 -*-
import datetime
import hashlib
import random
import sys
import time

import requests

from AustialiaHouse.config.password import KEY
from AustialiaHouse.config.proxy import PROXY_IP
from AustialiaHouse.config.useragent import get_user_agent


class HttpHelp():
    def __init__(self):
        pass

    def wwww(self, str):
        file_object = open('log.txt', 'w')
        try:
            file_object.write(str)
        finally:
            file_object.close()




# 得到代理
def get_proxy():
    _version = sys.version_info

    is_python3 = (_version[0] == 3)

    orderno = "ZF201710182445Nmtc1Q"
    secret = KEY

    timestamp = str(int(time.time()))  # 计算时间戳
    string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp

    if is_python3:
        string = string.encode()

    md5_string = hashlib.md5(string).hexdigest()  # 计算sign
    sign = md5_string.upper()  # 转换成大写
    auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp

    return auth


def get_headers():
    ua = get_user_agent()
    headers = {"Proxy-Authorization": get_proxy(), "User-Agent": ua}
    return headers



def get_referer(url=''):
    headers = [
        'https://www.google.com/',
        'https://www.baidu.com/',
        'https://twitter.com/',
        'http://weibo.com/',
    ]
    if url.find("m.zhiwai.ai") > 1:
        headers = [
            'https://m.zhiwai.ai/',
        ]
    if url.find("www.zillow.com") > 1:
        headers = [
            'https://www.zillow.com/',
        ]
    return headers[random.randint(0, len(headers) - 1)]
