#!/usr/bin/env python
# -- coding:utf-8 --
# @Date: 2021/10/6 17:12
# @File: force_get_location.py

import asyncio
import os
import sys

from pyppeteer import launch
from bs4 import BeautifulSoup

"""
免费版&开发版key 使用pyppeteer获取正在预警的城市id

用户使用war-force启动Weather.py时会使用本程序获取官网上的预警列表第一个
并返回location-ID

初次使用pyppeteer需要下载chromium 无法下载请使用代理或VPN
"""


async def get_html():
    """
    使用pyppeteer加载动态页面
    并保存html至本地
    :return:
    """
    browser = await launch(args=['dumpio=True'])
    page = await browser.newPage()
    await page.goto('https://www.qweather.com/severe-weather-more')
    await page.screenshot()
    html = await page.content()
    with open(sys.path[1] + '/module/API/temp.html', 'w', encoding='utf-8') as write_file:
        write_file.write(html)
    await browser.close()


def get_location():
    """
    加载html分析url并返回参数
    注: 标签检索元素随时可能会失效(包括但不限于: 官方修改html标签, 官方关闭网站, 等等)
    :return:
    """

    asyncio.get_event_loop().run_until_complete(get_html())
    with open(sys.path[1] + '/module/API/temp.html', 'r', encoding='utf-8') as open_file:
        data = open_file.read()
    soup = BeautifulSoup(data, 'html.parser')
    element = soup.find(attrs={'class': 'c-severe-news-item__a'}).get('href')
    location = element.split('-')[-1].split('.')[0]
    os.remove('temp.html')
    return location
