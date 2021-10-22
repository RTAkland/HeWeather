#!/usr/bin/env python
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/10/21
# @File Name: EXTRA_pusher.py
import random

import pcqq
import requests
import json
from ruamel.yaml import YAML

with open('../config-owner.yml', 'r', encoding='utf-8') as f:
    config = YAML().load(f.read())

@pcqq.on_full('!!tq')
def returnWeather(session: pcqq.Session):
    location = config['request-settings']['location']
    key = config['request-settings']['key']
    city_name = config['only-view-settings']['city-name']
    req = requests.Session()
    req.trust_env = False
    r = req.get(
        f'https://devapi.qweather.com/v7/weather/now?location={location}&key={key}')
    data = json.loads(r.text)
    text = f"""
    {city_name}天气
    更新时间{data['updateTime'][11:-6]}
    天气状况: {data['now']['text']}
    当前温度: {data['now']['temp']}℃
    风向: {data['now']['windDir']} 风速: {data['now']['windSpeed']}级
    空气湿度: {data['now']['humidity']}%
    空气压强: {data['now']['pressure']}Pa

    [数据来自:和风天气]
    """
    msg = pcqq.MessageSegment()
    msg.AddText('    ')
    msg.AddAt(session.event.UserID)
    msg.AddText(text)
    session.send(msg)


pcqq.init()
pcqq.run()

