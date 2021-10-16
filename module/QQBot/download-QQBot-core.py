#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/10/16
# @File Name: download-QQBot-core.py

import requests
import os

def down(system):
    if system == 'nt':
        windows_core = requests.get(
            'https://codechina.csdn.net/GeminiTay/some-rawpic/-/raw/master/go-cqhttp-w?inline=false')
        with open('go-cqhttp.exe', 'wb') as f:
            f.write(windows_core.content)
    else:
        linux_core = requests.get(
            'https://codechina.csdn.net/GeminiTay/some-rawpic/-/raw/master/go-cqhttp-linux?inline=false')
        with open('go-cqhttp-linux', 'wb') as f:
            f.write(linux_core.content)


if __name__ == '__main__':
    print('正在下载文件中...')
    down(os.name)
    print('执行完成...')
