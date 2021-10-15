#!/usr/bin/env python
# -- coding:utf-8 --
# @Date: 2021/10/9 21:10
# @File: SearchCity.py

import getpass
import time
import sys
import pandas as pd

from ruamel.yaml import YAML


def get_log_time():
    """
    获取时间
    :return: 格式化时间
    """
    return time.strftime("[%H:%M:%S]", time.localtime())


def read_excel(kw):
    """
    读取城市列表并根据传入的参数进行搜索
    :param kw: 进行匹配的关键字
    :return: city_list
    """
    index_count = 0
    city_list = []
    print(f'{get_log_time()}读取文件中...')
    df = pd.read_excel(sys.path[1] + '/assets/resources/China-City-List.xlsx')
    pd.set_option('max_rows', None)  # 读取xlsx文件不折叠
    data_records = df.to_dict(orient='split')
    for i in data_records['data']:
        if kw in str(i):
            print(f'{get_log_time()} {index_count} {i[2]}-{i[4]}-{i[6]}')
            index_count += 1
            city_list.append(i)
    if not city_list:
        return False
    return city_list


if __name__ == '__main__':
    yaml = YAML()
    keyword = input(f'{get_log_time()}输入城市名进行搜索:')
    if keyword:
        result = read_excel(keyword)
        if result:
            try:
                select_index = int(input(f'{get_log_time()}请输入数据前的索引选择城市:'))
                with open('config.yml', 'r', encoding='utf-8') as of:
                    data = yaml.load(of)

                    data['request-settings']['location'] = result[select_index][0]
                    data['only-view-settings'][
                        'city-name'] = f'{result[select_index][2]}-{result[select_index][4]}-{result[select_index][6]} '
                    data['only-view-settings']['time'] = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
                    data['only-view-settings']['user'] = getpass.getuser()

                with open('config.yml', 'w', encoding='utf-8') as wf:
                    yaml.dump(data, wf)
                input(f'{get_log_time()}写入完成...')
                sys.exit(0)
            except ValueError:
                print(f'{get_log_time()}[ERROR]请正确输入索引...')
                sys.exit(1)
    else:
        print(f'{get_log_time()}[ERROR]无关键字...')
        sys.exit(1)

