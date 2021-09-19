"""
Date:21/9/19
"""

import json
import smtplib
import sys
import time
import argparse
from concurrent.futures import ThreadPoolExecutor
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


import requests
import yaml

with open('config.yaml', 'r', encoding='gbk') as f: # 读取配置
    content = yaml.load(f.read(), Loader=yaml.Loader)

def get_log_time():
    return time.strftime("[%H:%M:%S]", time.localtime())

class mode_free:
    def __init__(self):
        self.key = content['key']
        self.city_name = content['city_name']
        self.location = int(content['location'])
        self.sender = content['sender']
        self.password = content['password']
        self.receiver = content['receiver']
        self.server = content['server']
        self.port = content['port']
        self.send_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.f_info_url = f'https://devapi.qweather.com/v7/weather/3d?location={self.location}&key={self.key}'

    def f_getdayinfo(self):
        f_session = requests.Session()
        f_session.trust_env = False
        f_request = f_session.get(self.f_info_url).text
        f_weather = json.loads(f_request)

        day_1 = f_weather['daily'][0]
        day_2 = f_weather['daily'][1]
        day_3 = f_weather['daily'][2]

        """
        fxDate : 日期
        textDay : 白天天气
        textNight : 夜间天气
        sunset : 日出时间
        sunrise : 日落时间
        humidity : 相对湿度
        tempMax : 最高气温
        tempMin : 最低气温
        iconDay : 白天的天气图标
        iconNight : 夜间的天气图标
        """

        date_1 = day_1['fxDate']
        date_2 = day_2['fxDate']
        date_3 = day_3['fxDate']

        day_weather_1 = day_1['textDay']
        day_weather_2 = day_2['textDay']
        day_weather_3 = day_3['textDay']

        night_weather_1 = day_1['textNight']
        night_weather_2 = day_2['textNight']
        night_weather_3 = day_3['textNight']

        sunset_1 = day_1['sunset']
        sunset_2 = day_2['sunset']
        sunset_3 = day_3['sunset']

        sunrise_1 = day_1['sunrise']
        sunrise_2 = day_2['sunrise']
        sunrise_3 = day_3['sunrise']

        humidity_1 = day_1['humidity']
        humidity_2 = day_2['humidity']
        humidity_3 = day_3['humidity']

        temperature_max_1 = day_1['tempMax']
        temperature_max_2 = day_2['tempMax']
        temperature_max_3 = day_3['tempMax']

        temperature_min_1 = day_1['tempMin']
        temperature_min_2 = day_2['tempMin']
        temperature_min_3 = day_3['tempMin']

        icon_day_1 = day_1['iconDay']
        icon_day_2 = day_2['iconDay']
        icon_day_3 = day_3['iconDay']

        icon_night_1 = day_1['iconNight']
        icon_night_2 = day_2['iconNight']
        icon_night_3 = day_3['iconNight']

        message = MIMEMultipart('related')
        message['From'] = Header('Weather System', 'utf-8')
        message['To'] = Header('Mail', 'utf-8')
        message['Subject'] = 'Weather'
        msg_content = MIMEMultipart('alternative')
        mail_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                <meta charset="utf-8">
                <title>Weather</title>
                </head>
                <body>
                <h2 align = 'center'>{self.city_name}天气</h2>
                <p  align = 'center'><i>发送者账号: {self.sender}<br>发送时间: {self.send_time}</i></p>
                <p align = 'center'>
                更新时间{date_1}<br>
                白天的天气是{day_weather_1}<img src="cid:img1" width="32" height="32">  晚上的天气是{night_weather_1}<img src="cid:img2" width="32" height="32"><br>
                当天日出时间:{sunrise_1}   日落时间:{sunset_1}<br>
                当天最高气温{temperature_max_1}℃   最低气温{temperature_min_1}℃<br>
                周围空气湿度{humidity_1}%<br>
                ==================================
                </p>
                </p>
            <h2 align = 'center'>{date_2} 天气(预测)</h2>
            <p align = 'center'>
                白天的天气是 {day_weather_2}<img src="cid:img3" width="32" height="32">  晚上的天气是 {night_weather_2}<img src="cid:img4" width="32" height="32"><br>
                当天日出时间:{sunrise_2}   日落时间:{sunset_2}<br>
                当天最高气温{temperature_max_2}℃   最低气温{temperature_min_2}℃<br>
                周围空气湿度{humidity_2}%<br>
            </p>

            <h2 align = 'center'>{date_3} 天气(预测)</h2>
            <p align = 'center'>
                白天的天气是{day_weather_3}<img src="cid:img5" width="32" height="32">  晚上的天气是 {night_weather_3}<img src="cid:img6" width="32" height="32"><br>
                当天日出时间:{sunrise_3}   日落时间:{sunset_3}<br>
                当天最高气温{temperature_max_3}℃   最低气温{temperature_min_3}℃<br>
                周围空气湿度{humidity_3}%<br>
            </p>
            <p align = 'center'>Send mode:{run_mode}</p>
                </body>
                </html>"""
        msg_content.attach(MIMEText(mail_html, 'html', 'utf-8'))
        message.attach(msg_content)

        with open(r'assets\{}.png'.format(icon_day_1), 'rb') as f:
            img1 = MIMEImage(f.read())
        with open(r'assets\{}.png'.format(icon_day_2), 'rb') as f:
            img2 = MIMEImage(f.read())
        with open(r'assets\{}.png'.format(icon_day_3), 'rb') as f:
            img3 = MIMEImage(f.read())

        with open(r'assets\{}.png'.format(icon_night_1), 'rb') as f:
            img4 = MIMEImage(f.read())
        with open(r'assets\{}.png'.format(icon_night_2), 'rb') as f:
            img5 = MIMEImage(f.read())
        with open(r'assets\{}.png'.format(icon_night_3), 'rb') as f:
            img6 = MIMEImage(f.read())

        img1.add_header('Content-ID', 'img1')
        img2.add_header('Content-ID', 'img2')
        img3.add_header('Content-ID', 'img3')
        img4.add_header('Content-ID', 'img4')
        img5.add_header('Content-ID', 'img5')
        img6.add_header('Content-ID', 'img6')

        message.attach(img1)
        message.attach(img2)
        message.attach(img3)
        message.attach(img4)
        message.attach(img5)
        message.attach(img6)

        try:
            smtp = smtplib.SMTP_SSL(self.server, self.port)
            smtp.login(self.sender, self.password)
            smtp.sendmail(self.sender, self.receiver, message.as_string())
        except smtplib.SMTPException as e:
            print(f'{get_log_time()}邮件发送错误', e)

class mode_dev:
    def __init__(self):
        self.key = content['key']
        self.city_name = content['city_name']
        self.location = content['location']
        self.sender = content['sender']
        self.password = content['password']
        self.receiver = content['receiver']
        self.server = content['server']
        self.port = content['port']
        self.send_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.info_url = f'https://devapi.qweather.com/v7/weather/7d?location={self.location}&key={self.key}'
        self.indices = f'https://devapi.qweather.com/v7/indices/1d?type=1,2&location={self.location}&key={self.key}'
    def getdayinfo(self):
        session = requests.Session()
        session.trust_env = False # 使用本地网络
        r_day = session.get(self.info_url).text
        r_indices = session.get(self.indices).text
        weather_day_text = json.loads(r_day)
        weather_indices = json.loads(r_indices)
        indices = weather_indices['daily'][0]
        daily_name = indices['name']
        daily_category = indices['category']

        day_1 = weather_day_text['daily'][0]
        day_2 = weather_day_text['daily'][1]
        day_3 = weather_day_text['daily'][2]
        day_4 = weather_day_text['daily'][3]
        day_5 = weather_day_text['daily'][4]
        day_6 = weather_day_text['daily'][5]
        day_7 = weather_day_text['daily'][6]
        # Begin
        date_1 = day_1['fxDate']
        date_2 = day_2['fxDate']
        date_3 = day_3['fxDate']
        date_4 = day_4['fxDate']
        date_5 = day_5['fxDate']
        date_6 = day_6['fxDate']
        date_7 = day_7['fxDate']

        day_weather_1 = day_1['textDay']
        day_weather_2 = day_2['textDay']
        day_weather_3 = day_3['textDay']
        day_weather_4 = day_4['textDay']
        day_weather_5 = day_5['textDay']
        day_weather_6 = day_6['textDay']
        day_weather_7 = day_7['textDay']

        night_weather_1 = day_1['textNight']
        night_weather_2 = day_2['textNight']
        night_weather_3 = day_3['textNight']
        night_weather_4 = day_4['textNight']
        night_weather_5 = day_5['textNight']
        night_weather_6 = day_6['textNight']
        night_weather_7 = day_7['textNight']

        sunset_1 = day_1['sunset']
        sunset_2 = day_2['sunset']
        sunset_3 = day_3['sunset']
        sunset_4 = day_4['sunset']
        sunset_5 = day_5['sunset']
        sunset_6 = day_6['sunset']
        sunset_7 = day_7['sunset']

        sunrise_1 = day_1['sunrise']
        sunrise_2 = day_2['sunrise']
        sunrise_3 = day_3['sunrise']
        sunrise_4 = day_4['sunrise']
        sunrise_5 = day_5['sunrise']
        sunrise_6 = day_6['sunrise']
        sunrise_7 = day_7['sunrise']

        humidity_1 = day_1['humidity']
        humidity_2 = day_2['humidity']
        humidity_3 = day_3['humidity']
        humidity_4 = day_4['humidity']
        humidity_5 = day_5['humidity']
        humidity_6 = day_6['humidity']
        humidity_7 = day_7['humidity']

        temperature_max_1 = day_1['tempMax']
        temperature_max_2 = day_2['tempMax']
        temperature_max_3 = day_3['tempMax']
        temperature_max_4 = day_4['tempMax']
        temperature_max_5 = day_5['tempMax']
        temperature_max_6 = day_6['tempMax']
        temperature_max_7 = day_7['tempMax']

        temperature_min_1 = day_1['tempMin']
        temperature_min_2 = day_2['tempMin']
        temperature_min_3 = day_3['tempMin']
        temperature_min_4 = day_4['tempMin']
        temperature_min_5 = day_5['tempMin']
        temperature_min_6 = day_6['tempMin']
        temperature_min_7 = day_7['tempMin']

        icon_day_1 = day_1['iconDay']
        icon_day_2 = day_2['iconDay']
        icon_day_3 = day_3['iconDay']
        icon_day_4 = day_4['iconDay']
        icon_day_5 = day_5['iconDay']
        icon_day_6 = day_6['iconDay']
        icon_day_7 = day_7['iconDay']

        icon_night_1 = day_1['iconNight']
        icon_night_2 = day_2['iconNight']
        icon_night_3 = day_3['iconNight']
        icon_night_4 = day_4['iconNight']
        icon_night_5 = day_5['iconNight']
        icon_night_6 = day_6['iconNight']
        icon_night_7 = day_7['iconNight']

        daily_type = f'{daily_name}:{daily_category}' # 指数类型 & 建议
        indices_tip = indices['text'] # 建议

        message = MIMEMultipart('related')
        message['From'] = Header('Weather System', 'utf-8')
        message['To'] = Header('Mail', 'utf-8')
        message['Subject'] = 'Weather'
        msg_content = MIMEMultipart('alternative')
        mail_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <title>Weather</title>
        </head>
        <body>
        <h2 align = 'center'>{self.city_name}今天天气</h2>
        <p  align = 'center'><i>发送者账号: {self.sender}<br>发送时间: {self.send_time}</i></p>
        <p align = 'center'>
        更新时间{date_1}<br>
        白天的天气是{day_weather_1}<img src="cid:img1" width="32" height="32">  晚上的天气是{night_weather_1}<img src="cid:img2" width="32" height="32"><br>
        当天日出时间:{sunrise_1}   日落时间:{sunset_1}<br>
        当天最高气温{temperature_max_1}℃   最低气温{temperature_min_1}℃<br>
        周围空气湿度{humidity_1}%<br>
        {daily_type}<br>
        {indices_tip}<br>
        ==================================
        </p>
        </p>
    <h2 align = 'center'>{date_2} 天气(预测)</h2>
    <p align = 'center'>
        白天的天气是 {day_weather_2}<img src="cid:img3" width="32" height="32">  晚上的天气是 {night_weather_2}<img src="cid:img4" width="32" height="32"><br>
        当天日出时间:{sunrise_2}   日落时间:{sunset_2}<br>
        当天最高气温{temperature_max_2}℃   最低气温{temperature_min_2}℃<br>
        周围空气湿度{humidity_2}%<br>
    </p>
    
    <h2 align = 'center'>{date_3} 天气(预测)</h2>
    <p align = 'center'>
        白天的天气是{day_weather_3}<img src="cid:img5" width="32" height="32">  晚上的天气是 {night_weather_3}<img src="cid:img6" width="32" height="32"><br>
        当天日出时间:{sunrise_3}   日落时间:{sunset_3}<br>
        当天最高气温{temperature_max_3}℃   最低气温{temperature_min_3}℃<br>
        周围空气湿度{humidity_3}%<br>
    </p>
    
    <h2 align = 'center'>{date_4} 天气(预测)</h2>
    <p align = 'center'>
        白天的天气是 {day_weather_4}<img src="cid:img7" width="32" height="32">  晚上的天气是 {night_weather_4}<img src="cid:img8" width="32" height="32"><br>
        当天日出时间:{sunrise_4}   日落时间:{sunset_4}<br>
        当天最高气温{temperature_max_4}℃   最低气温{temperature_min_4}℃<br>
        周围空气湿度{humidity_4}%<br>
    </p>
    
    <h2 align = 'center'>{date_5} 天气(预测)</h2>
    <p align = 'center'>
        白天的天气是 {day_weather_5}<img src="cid:img9" width="32" height="32">  晚上的天气是 {night_weather_5}<img src="cid:img10" width="32" height="32"><br>
        当天日出时间:{sunrise_5}   日落时间:{sunset_5}<br>
        当天最高气温{temperature_max_5}℃   最低气温{temperature_min_5}℃<br>
        周围空气湿度{humidity_5}%<br>
    </p>
    
    <h2 align = 'center'>{date_6} 天气(预测)</h2>
    <p align = 'center'>
        白天的天气是 {day_weather_6}<img src="cid:img11" width="32" height="32">  晚上的天气是 {night_weather_6}<img src="cid:img12" width="32" height="32"><br>
        当天日出时间:{sunrise_6}   日落时间:{sunset_6}<br>
        当天最高气温{temperature_max_6}℃   最低气温{temperature_min_6}℃<br>
        周围空气湿度{humidity_6}%<br>
    </p>
    
    <h2 align = 'center'>{date_7} 天气(预测)</h2>
    <p align = 'center'>
        白天的天气是 {day_weather_7}<img src="cid:img13" width="32" height="32">  晚上的天气是 {night_weather_7}<img src="cid:img14" width="32" height="32"><br>
        当天日出时间:{sunrise_7}   日落时间:{sunset_7}<br>
        当天最高气温{temperature_max_7}℃   最低气温{temperature_min_7}℃<br>
        周围空气湿度{humidity_7}%<br>
    </p>
    <p align = 'center'>Send mode:{run_mode}</p>
        </body>
        </html>"""
        msg_content.attach(MIMEText(mail_html, 'html', 'utf-8'))
        message.attach(msg_content)

        with open(r'assets\{}.png'.format(icon_day_1), 'rb') as f:
            img1 = MIMEImage(f.read())
        with open(r'assets\{}.png'.format(icon_day_2), 'rb') as f:
            img2 = MIMEImage(f.read())
        with open(r'assets\{}.png'.format(icon_day_3), 'rb') as f:
            img3 = MIMEImage(f.read())
        with open(r'assets\{}.png'.format(icon_day_4), 'rb') as f:
            img4 = MIMEImage(f.read())
        with open(r'assets\{}.png'.format(icon_day_5), 'rb') as f:
            img5 = MIMEImage(f.read())
        with open(r'assets\{}.png'.format(icon_day_6), 'rb') as f:
            img6 = MIMEImage(f.read())
        with open(r'assets\{}.png'.format(icon_day_7), 'rb') as f:
            img7 = MIMEImage(f.read())

        with open(r'assets\{}.png'.format(icon_night_1), 'rb') as f:
            img8 = MIMEImage(f.read())
        with open(r'assets\{}.png'.format(icon_night_2), 'rb') as f:
            img9 = MIMEImage(f.read())
        with open(r'assets\{}.png'.format(icon_night_3), 'rb') as f:
            img10 = MIMEImage(f.read())
        with open(r'assets\{}.png'.format(icon_night_4), 'rb') as f:
            img11 = MIMEImage(f.read())
        with open(r'assets\{}.png'.format(icon_night_5), 'rb') as f:
            img12 = MIMEImage(f.read())
        with open(r'assets\{}.png'.format(icon_night_6), 'rb') as f:
            img13 = MIMEImage(f.read())
        with open(r'assets\{}.png'.format(icon_night_7), 'rb') as f:
            img14 = MIMEImage(f.read())

        img1.add_header('Content-ID', 'img1')
        img2.add_header('Content-ID', 'img2')
        img3.add_header('Content-ID', 'img3')
        img4.add_header('Content-ID', 'img4')
        img5.add_header('Content-ID', 'img5')
        img6.add_header('Content-ID', 'img6')
        img7.add_header('Content-ID', 'img7')
        img8.add_header('Content-ID', 'img8')
        img9.add_header('Content-ID', 'img9')
        img10.add_header('Content-ID', 'img10')
        img11.add_header('Content-ID', 'img11')
        img12.add_header('Content-ID', 'img12')
        img13.add_header('Content-ID', 'img13')
        img14.add_header('Content-ID', 'img14')

        message.attach(img1)
        message.attach(img2)
        message.attach(img3)
        message.attach(img4)
        message.attach(img5)
        message.attach(img6)
        message.attach(img7)
        message.attach(img8)
        message.attach(img9)
        message.attach(img10)
        message.attach(img11)
        message.attach(img12)
        message.attach(img13)
        message.attach(img14)

        try:
            smtp = smtplib.SMTP_SSL(self.server, self.port)
            smtp.login(self.sender, self.password)
            smtp.sendmail(self.sender, self.receiver, message.as_string())
        except smtplib.SMTPException as e:
            print(f'{get_log_time()}邮件发送错误', e)

if __name__ == '__main__':
    executor = ThreadPoolExecutor(max_workers=2)  # 线程池
    run_mode = content['mode']  # 发送邮件的模式
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', help='Run with test mode')
    args = parser.parse_args().test
    if args:# 测试模式
        if args == 'test':
            run_mode = 'Test mode'
            mode_dev().getdayinfo()
            input(f'{get_log_time()}使用了测试模式发送了一封邮件至 {content["receiver"]}')
            sys.exit(0)
        else:
            print(f'{get_log_time()}请使用正确的参数启动')

    print(f'{get_log_time()}请确保config.yaml内的参数正确, 否则将无法发送邮件\n')
    for cfg_checker in content.values():
        if cfg_checker == None:
            input(f'{get_log_time()}配置文件错误 回车退出')
            sys.exit(0)
    if run_mode == 'dev':
        while True:
            time_local = time.strftime("%H:%M", time.localtime())
            for i in content['time']:
                print(i)
                print(f'{get_log_time()}运行中  工作模式: Dev 发送时间:{content["time"]}')
                time.sleep(5)
                if time_local == i:
                    executor.submit(mode_dev().getdayinfo)
                    executor.shutdown()
                    print(f'{get_log_time()}正在发送邮件...')
                    time.sleep(61)
    elif run_mode == 'free':
        while True:
            time_local = time.strftime("%H:%M", time.localtime())
            for i in content['time']:
                print(f'{get_log_time()}运行中  工作模式: Free 发送时间:{content["time"]}')
                time.sleep(5)
                if time_local == i:
                    executor.submit(mode_free().f_getdayinfo)
                    executor.shutdown()
                    print(f'{get_log_time()}正在发送邮件...')
                    time.sleep(61)






