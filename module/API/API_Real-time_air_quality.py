#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/10/13 下午8:45
# @File: API_Real-time_air_quality.py

"""
开发版key获取实时空气质量
only: Dev-mode
"""

import requests
import json
from ruamel.yaml import YAML


def real_time_air_quality():
    yaml = YAML()
    with open('../../config.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f.read())

        mode = config['request-settings']['mode']
        key = config['request-settings']['key']
        location = config['request-settings']['location']
        unit = config['request-settings']['unit']
        lang = config['request-settings']['lang']

    with open('../../assets/resources/code.json', 'r', encoding='utf-8') as code_file:
        code_status = json.loads(code_file.read())

    if mode != 'dev':
        return False, print('Only Dev-mode')
    r = requests.get(f'https://devapi.qweather.com/v7/air/now?'
                     f'location={location}config.yml&key={key}&lang={lang}&unit={unit}&gzip=y')
    _data = json.loads(r.text)

    return code_status[_data['code']], _data['now']

