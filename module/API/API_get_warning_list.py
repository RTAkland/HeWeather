#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/10/13 下午9:18
# @File: API_get_warning_list.py

"""
开发版key使用此API可以快速返回正在预警的城市id
Only Dev-mode
"""

import requests
import json
from ruamel.yaml import YAML

def get_warning_list(_range='cn'):
    yaml = YAML()
    with open('../../config.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f.read())
    with open('../../assets/resources/code.json', 'r', encoding='utf-8') as code_file:
        code_status = json.loads(code_file.read())

        key = config['request-settings']['key']
        unit = config['request-settings']['unit']
        lang = config['request-settings']['lang']
    r = requests.get(f'https://devapi.qweather.com/v7/warning/list?range={_range}&key={key}&lang={lang}&unit={unit}')
    _data = json.loads(r.text)

    return code_status[_data['code']], _data['warningLocList'][0]['locationId']
