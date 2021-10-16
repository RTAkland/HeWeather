#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/10/16
# @File Name: sendToQQ.py
import json
import socket
import sys
import time
import requests
from ruamel.yaml import YAML

print(f'{time.strftime("[%H:%M:%S]", time.localtime())}QQBot Running')

yaml = YAML()
with open(sys.path[1] + '/config.yml') as f:
    config = yaml.load(f.read())
    key = config['request-settings']['key']
    location = config['request-settings']['location']
    city_name = config['only-view-settings']['city-name']
    _keyword = config['EXTRA']['QQBOT']['Keyword']


def send_msg(_type, qq):
    r = requests.get(f'https://devapi.qweather.com/v7/weather/now?location={location}&key={key}').text
    weather_req = json.loads(r)
    weather_info = f"""
    地区:{city_name}
    更新时间:今天{weather_req['updateTime'][10:-6]}
    当前天气:{weather_req['now']['text']}
    当前温度:{weather_req['now']['temp']}℃
    风向:{weather_req['now']['windDir']}
    风速:{weather_req['now']['windSpeed']}m/s
    空气湿度:{weather_req['now']['humidity']}%
    气压:{weather_req['now']['pressure']}Pa
    
    数据来自: 和风天气
    """
    if _type == 'p':
        requests.get(f'http://127.0.0.1:5700/send_private_msg?user_id={qq}&message={weather_info}')
    else:
        requests.get(f'http://127.0.0.1:5700/send_group_msg?group_id={qq}&message=test')


def rev_msg_manual():
    while True:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('127.0.0.1', 8000))
        server.listen(10)
        conn, address = server.accept()
        msg = conn.recv(10240).decode('utf-8')
        if "!!" in msg:
            if msg is not None:
                if 'group' not in msg:
                    message = msg.split(':')[10].split(',')[0][1:-1]
                    sender = msg.split(':')[20].split(',')[0][:-1]
                    if message == '!!tq':
                        send_msg('p', sender, )
                else:
                    print('else')
                    print(msg.split(':'))
                    group_id = msg.split(':')[11].split(',')[0]
                    # sender_id = msg.split(':')[28].split(',')[0][:-1]  # at ones Not available
                    message = msg.split(':')[12].split(',')[0][1:-1]
                    if message == _keyword:
                        send_msg('g', group_id)

