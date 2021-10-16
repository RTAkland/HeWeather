#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/10/16
# @File Name: download-QQBot-core.py

import requests

windows_core = requests.get('https://gitee.com/rtakland/prefile-repo/raw/main/go-cqhttp.exe')
with open('go-cqhttp.exe', 'wb') as f:
    f.write(windows_core.content)

linux_core = requests.get('https://gitee.com/rtakland/prefile-repo/raw/main/go-cqhttp-linux')
with open('go-cqhttp-linux', 'wb') as f:
    f.write(linux_core.content)

print('执行完成...')