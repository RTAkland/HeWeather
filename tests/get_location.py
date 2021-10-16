#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/9/29
# @File Name: get_location.py


from requests import Session


class RequestWebsite:
    def __init__(self):
        self.url = 'https://ip.tool.lu/'

    def request(self):
        __session = Session()
        __session.trust_env = False
        __r = __session.get(self.url, timeout=5).text
        return {'IP:': __r.split(':')[1].split()[0], 'Location': __r.split(':')[2].split()}  # return IP & Cities
