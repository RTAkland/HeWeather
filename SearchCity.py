import time
import sys
import os
import pandas as pd
import yaml


def time_now(): # 获取时间
    return time.strftime("[%H:%M:%S]", time.localtime())

def read_excel(keyword):
    print(f'{time_now()}读取文件中...\n')
    global lst_count
    df = pd.read_excel('China-City-List.xlsx')
    pd.set_option('max_rows', None) # 读取xlsx文件不折叠
    data_records = df.to_dict(orient='split')
    for i in data_records['data']:
        if keyword in str(i):
            city_lst.append(i)
            print(f'{time_now()} {lst_count} {i[2]}-{i[4]}-{i[6]}-{i[8]}')
            lst_count += 1
    print(f'\n{time_now()}搜索到{lst_count}个结果 从左往右等级逐次提高 上滑继续寻找城市')

def init(): # 初始化配置文件
    config = {
        'mode': 'free',
        'CHANGE_TIME': str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' Changer:' + os.getlogin()),
        'city_name': None,
        'key': None,
        'location': None,
        'password': None,
        'port': 465,
        'receiver': None,
        'sender': None,
        'server': None,
        'time': ['08:00',
                 '12:00'
                 ]
    }
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, Dumper=yaml.Dumper)
    input(f'{time_now()}配置文件初始化完成 回车退出...')
    sys.exit(0)


if __name__ == '__main__':
    lst_count = 0
    city_lst = []
    print(f'{time_now()}通过"init"关键字来初始化配置文件 选择结束后会修改文件内的"city_name" "location" "CHANGE_TIME"项')
    operation = input(f'{time_now()}想要搜索的关键字:')
    if operation == 'init':
        init()
    else:
        read_excel(operation)
    if lst_count == 0:
        input(f'{time_now()}无搜索结果 回车退出...')
        sys.exit(0)
    elif lst_count == 1:
        with open('config.yaml') as fp:
            doc = yaml.load(fp, Loader=yaml.Loader)
            city_names = f'{city_lst[0][1]} - {city_lst[0][4]} - {city_lst[0][6]} - {city_lst[0][8]}'
            doc['location'] = int(city_lst[0][0])
            doc['city_name'] = str(city_names)
            doc['CHANGE_TIME'] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' Changer:' + os.getlogin())

        with open('config.yaml', 'w') as f:
            yaml.dump(doc, f, allow_unicode=True)
        input(f'{time_now()}精确搜索直接写入文件 回车退出...')
        sys.exit(0)
    else:
        try:
            select_city = int(input(f'{time_now()}输入数据开头索引数字写入配置:'))
            with open('config.yaml') as fp:
                city_names = f'{city_lst[select_city][2]} - {city_lst[select_city][4]} - {city_lst[select_city][6]} - {city_lst[select_city][8]}'
                doc = yaml.load(fp, Loader=yaml.Loader)
                doc['location'] = int(city_lst[select_city][0])
                doc['city_name'] = str(city_names)
                doc['CHANGE_TIME'] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' Changer:' + os.getlogin())

            with open('config.yaml', 'w') as f:
                    yaml.dump(doc, f, allow_unicode=True)
            input(f'{time_now()}写入完成 回车退出...')
            sys.exit(0)
        except Exception as e:
            print(e)
            input(f'{time_now()}写入错误 回车退出...')
            sys.exit(0)

