#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/10/13 下午8:45
# @File: API_Real-time_air_quality.py

"""
Get Real-time air quality from API and return data
only: Dev-mode
"""

import requests
import json
from ruamel.yaml import YAML


def real_time_air_quality_args():
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
                     f'location={location}&key={key}&lang={lang}&unit={unit}&gzip=y')
    _data = json.loads(r.text)

    req_status = code_status[_data['code']]
    return req_status, _data['now']
