#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/9/29
# @File Name: Weather.py


import argparse
import json
import random
import smtplib
import sys
import time
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from multiprocessing import Process

import requests
from ruamel.yaml import YAML
from module import API_get_locationID
from module import API_get_warning_list


class SendWeatherMail:
    def __init__(self):
        self.location = my_config['request-settings']['location']  # 城市ID
        self.key = my_config['request-settings']['key']  # API密钥
        self.city_name = my_config['only-view-settings']['city-name']  # 城市名称仅作邮件内容
        self.sender = my_config['mail-settings']['sender']  # 发送者邮箱
        self.password = my_config['mail-settings']['password']  # 服务器登录密码
        self.receiver = my_config['other-settings']['receiver']  # 接收者邮箱 --> 列表 [无论有几个人都必须是列表]
        self.server = my_config['mail-settings']['server']  # 邮箱服务器
        self.port = my_config['mail-settings']['port']  # 邮箱端口号
        self.unit = my_config['request-settings']['unit']  # 度量单位
        self.lang = my_config['request-settings']['lang']  # 语言
        self.icon_style = my_config['other-settings']['icon-style']  # 天气图标
        self.mode = my_config['request-settings']['mode']  # 发送模式 --仅作判断标识
        self.send_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 发送时间

        if arg_test == 'war-force':  # 如果运行参数是war-force则替换self.location
            if self.mode != 'dev':  # 如果发送模式不是dev则使用爬虫方式获取城市id
                self.location = API_get_locationID.get_location()
            self.location = API_get_warning_list.get_warning_list()[1]
        self.Dev_Link = f'https://devapi.qweather.com/v7/weather/7d?location=' \
                        f'{self.location}&key={self.key}&unit={self.unit}&lang={self.lang}'

        self.indices = f'https://devapi.qweather.com/v7/indices/1d?type=1,2&location=' \
                       f'{self.location}&key={self.key}&unit={self.unit}&lang={self.lang}'

        self.Free_Link = f'https://devapi.qweather.com/v7/weather/3d?location=' \
                         f'{self.location}&key={self.key}&unit={self.unit}&lang={self.lang} '

        self.codes = json.loads(open('./assets/resources/code.json', 'r', encoding='utf-8').read())
        self.message = MIMEMultipart('related')
        self.message['From'] = Header('HeWeatherReporter')  # 发件人名称
        self.message['To'] = Header('All allowed User')  # 收件人显示名称
        self.msg_content = MIMEMultipart('alternative')  # 文字目录

        self.smtp = smtplib.SMTP_SSL(self.server, self.port)  # 登录服务器 使用SSL链接

    def Dev_mode(self):
        """

        开发版获取天气信息及处理信息
        Date : 日期
        day_weather : 白天天气
        night_weather : 夜间天气
        sunset : 日出时间
        sunrise : 日落时间
        humidity : 相对湿度
        tempMax : 最高气温
        tempMin : 最低气温
        iconDay : 白天的天气图标
        iconNight : 夜间的天气图标
        returnCode : 返回代码
        :return:
        """
        r_day = requests.get(self.Dev_Link, headers={'Accept-Encoding': 'gzip'}).text
        r_indices = requests.get(self.indices, headers={'Accept-Encoding': 'gzip'}).text
        weather_day_text = json.loads(r_day)  # 使用json加载数据
        weather_indices = json.loads(r_indices)
        returnCode_weather = weather_day_text['code']
        returnCode_indices = weather_indices['code']
        print(f'{Other().log_time}天气信息请求结果:{self.codes[returnCode_weather]} '
              f'生活建议请求结果:{self.codes[returnCode_indices]}')
        indices = weather_indices['daily'][0]
        daily_type = f'{indices["name"]}:{indices["category"]}'  # 指数类型 & 建议
        try:
            indices_tip = indices['text']
        except ValueError:
            indices_tip = '无具体描述'

        # 1-7天数据
        day_1 = weather_day_text['daily'][0]
        day_2 = weather_day_text['daily'][1]
        day_3 = weather_day_text['daily'][2]
        day_4 = weather_day_text['daily'][3]
        day_5 = weather_day_text['daily'][4]
        day_6 = weather_day_text['daily'][5]
        day_7 = weather_day_text['daily'][6]

        date = [day_1['fxDate'], day_2['fxDate'], day_3['fxDate'], day_4['fxDate'], day_5['fxDate'], day_6['fxDate'],
                day_7['fxDate']]
        day_weather = [day_1['textDay'], day_2['textDay'], day_3['textDay'], day_4['textDay'], day_5['textDay'],
                       day_6['textDay'], day_7['textDay']]
        night_weather = [day_1['textNight'], day_2['textNight'], day_3['textNight'], day_4['textNight'],
                         day_5['textNight'], day_6['textNight'], day_7['textNight']]
        sunset = [day_1['sunset'], day_2['sunset'], day_3['sunset'], day_4['sunset'], day_5['sunset'], day_6['sunset'],
                  day_7['sunset']]
        sunrise = [day_1['sunrise'], day_2['sunrise'], day_3['sunrise'], day_4['sunrise'], day_5['sunrise'],
                   day_6['sunrise'], day_7['sunrise']]
        humidity = [day_1['humidity'], day_2['humidity'], day_3['humidity'], day_4['humidity'], day_5['humidity'],
                    day_6['humidity'], day_7['humidity']]
        temperature_max = [day_1['tempMax'], day_2['tempMax'], day_3['tempMax'], day_4['tempMax'], day_5['tempMax'],
                           day_6['tempMax'], day_7['tempMax']]
        temperature_min = [day_1['tempMin'], day_2['tempMin'], day_3['tempMin'], day_4['tempMin'], day_5['tempMin'],
                           day_6['tempMin'], day_7['tempMin']]
        # 邮件内容主体
        mail_html = f"""
        <!DOCTYPE html>
        <html>
        
          <head>
            <meta charset="utf-8" />
            <title>Weather</title>
          </head>
        
          <body>
            <div style="text-align: center;">
            <h2>{self.city_name}今天天气</h2>
              <p>
                <i>发送者账号: {self.sender}
                  <br />发送时间: {self.send_time}</i>
              </p>
              <p>更新时间:{date[0]}
                <br />白天的天气是{day_weather[0]}
                <sub><img src="cid:img1" width="25" height="25" /></sub>晚上的天气是{night_weather[0]}
                <sub><img src="cid:img2" width="25" height="25" /></sub>
                <br />当天日出时间:{sunrise[0]} 日落时间:{sunset[0]}
                <br />当天最高气温{temperature_max[0]}℃ 最低气温{temperature_min[0]}℃
                <br />周围空气湿度{humidity[0]}%
                <br />{daily_type}
                <br />
                <i>{indices_tip}</i>
                <br />==================================</p>
            </div>
            <div style="text-align: center;">
                <h2>{date[1]} 天气(预测)</h2>
                <p>白天的天气是{day_weather[1]}
                    <sub><img src="cid:img3" width="25" height="25" /></sub>晚上的天气是 {night_weather[1]}
                    <sub><img src="cid:img4" width="25" height="25" /></sub>
                    <br />当天日出时间:{sunrise[2]} 日落时间:{sunset[2]}
                    <br />当天最高气温{temperature_max[2]}℃ 最低气温{temperature_min[2]}℃
                    <br />周围空气湿度{humidity[2]}%
                    <br />
                </p>
            </div>
            <div style="text-align: center;">
                <h2>{date[2]} 天气(预测)</h2>
                <p>白天的天气是{day_weather[2]}
                    <sub><img src="cid:img5" width="25" height="25" /></sub>晚上的天气是 {night_weather[1]}
                    <sub><img src="cid:img6" width="25" height="25" /></sub>
                    <br />当天日出时间:{sunrise[2]} 日落时间:{sunset[2]}
                    <br />当天最高气温{temperature_max[2]}℃ 最低气温{temperature_min[2]}℃
                    <br />周围空气湿度{humidity[2]}%
                    <br /></p>
            </div>
            <div style="text-align: center;">
                <h2>{date[3]} 天气(预测)</h2>
                <p>白天的天气是 {day_weather[3]}
                    <sub><img src="cid:img7" width="25" height="25" /></sub>晚上的天气是 {night_weather[1]}
                    <sub><img src="cid:img8" width="25" height="25" /></sub>
                    <br />当天日出时间:{sunrise[3]} 日落时间:{sunset[3]}
                    <br />当天最高气温{temperature_max[3]}℃ 最低气温{temperature_min[3]}℃
                    <br />周围空气湿度{humidity[3]}%
                    <br /></p>
            </div>
            <div style="text-align: center;">
                <h2>{date[4]} 天气(预测)</h2>
                <p>白天的天气是 {day_weather[4]}
                    <sub><img src="cid:img9" width="25" height="25" /></sub>晚上的天气是 {night_weather[1]}
                    <sub><img src="cid:img10" width="25" height="25" /></sub>
                    <br />当天日出时间:{sunrise[4]} 日落时间:{sunset[4]}
                    <br />当天最高气温{temperature_max[4]}℃ 最低气温{temperature_min[4]}℃
                    <br />周围空气湿度{humidity[4]}%
                    <br /></p>
            </div>
            <div style="text-align: center;">
                <h2>{date[5]} 天气(预测)</h2>
                <p>白天的天气是 {day_weather[5]}
                    <sub><img src="cid:img11" width="25" height="25" /></sub>晚上的天气是 {night_weather[1]}
                    <sub><img src="cid:img12" width="25" height="25" /></sub>
                    <br />当天日出时间:{sunrise[5]} 日落时间:{sunset[5]}
                    <br />当天最高气温{temperature_max[5]}℃ 最低气温{temperature_min[5]}℃
                    <br />周围空气湿度{humidity[5]}%
                    <br /></p>
            </div>
            <div style="text-align: center;">
                <h2>{date[6]} 天气(预测)</h2>
                <p>白天的天气是{day_weather[2]}
                    <sub><img src="cid:img13" width="25" height="25" /></sub>晚上的天气是 {night_weather[1]}
                    <sub><img src="cid:img14" width="25" height="25" /></sub>
                    <br />当天日出时间:{sunrise[2]} 日落时间:{sunset[2]}
                    <br />当天最高气温{temperature_max[2]}℃ 最低气温{temperature_min[2]}℃
                    <br />周围空气湿度{humidity[2]}% <br /> <br /></p> </div> <div style="text-align: center; font-size: 
                    medium;"> <b> <a href="https://dev.qweather.com/" style="color: black;" target="_blank"> <img 
                    src="https://dev.qweather.com/assets/images/logo-s-dark.png" alt="QWeatherIcon" width="15" 
                    height="15" />和风天气开发平台</a> <br /> <a href="https://github.com/MarkusJoe/HeWeatherReporter" 
                    style="color: black;" target="_blank"> <img 
                    src="https://codechina.csdn.net/GeminiTay/some-rawpic/-/raw/master/fluidicon.png" 
                    alt="githubIcon" width="15" height="15" />Github仓库</a> </b> </div> </body> 
        
        </html>
                """
        self.message['Subject'] = '7天天气预报'  # 邮件标题
        self.message.attach(MIMEText(mail_html, 'html', 'utf-8'))

        icon_lst = [day_1['iconDay'], day_2['iconDay'], day_3['iconDay'], day_4['iconDay'], day_5['iconDay'],
                    day_6['iconDay'], day_7['iconDay'], day_1['iconNight'], day_2['iconNight'], day_3['iconNight'],
                    day_4['iconNight'], day_5['iconNight'], day_6['iconNight'], day_7['iconNight']]

        # 循环将图片attach到html里
        image_count = 1
        for image_resource in icon_lst:
            with open(f'./assets/{self.icon_style}/{image_resource}.png', 'rb') as fp:
                MyImage = MIMEImage(fp.read())
                MyImage.add_header('Content-ID', f'img{image_count}')
                self.message.attach(MyImage)
                image_count += 1
        try:
            self.smtp.login(self.sender, self.password)  # 登录
            self.smtp.sendmail(self.sender, self.receiver, self.message.as_string())  # 发送
        except smtplib.SMTPException as e:
            print(f'{Other().log_time}邮件发送错误', e)

    # 免费版本
    def Free_mode(self):
        f_request = requests.get(self.Free_Link, headers={'Accept-Encoding': 'gzip'}).text
        f_weather = json.loads(f_request)
        returnCode_weather = f_weather['code']
        print(f'{Other().log_time}天气信息请求结果:{self.codes[returnCode_weather]}')

        day_1 = f_weather['daily'][0]
        day_2 = f_weather['daily'][1]
        day_3 = f_weather['daily'][2]

        date = [day_1['fxDate'], day_2['fxDate'], day_2['fxDate']]
        day_weather = [day_1['textDay'], day_2['textDay'], day_2['textDay']]
        night_weather = [day_1['textNight'], day_2['textNight'], day_2['textNight']]
        sunset = [day_1['sunset'], day_2['sunset'], day_2['sunset']]
        sunrise = [day_1['sunrise'], day_2['sunrise'], day_2['sunrise']]
        humidity = [day_1['humidity'], day_2['humidity'], day_2['humidity']]
        temperature_max = [day_1['tempMax'], day_2['tempMax'], day_3['tempMax']]
        temperature_min = [day_1['tempMin'], day_2['tempMin'], day_2['tempMin']]
        icon_lst = [day_1['iconDay'], day_1['iconDay'], day_3['iconDay'], day_1['iconNight'], day_2['iconNight'],
                    day_3['iconNight']]

        mail_html = f"""
        <!DOCTYPE html>
        <html>
          
          <head>
            <meta charset="utf-8" />
            <title>Weather</title>
          </head>
        
          <body>
          <div style="text-align: center;">
            <h2>{self.city_name}今天天气</h2>
            <p>
              <i>发送者账号: {self.sender}
                <br />发送时间: {self.send_time}</i>
            </p>
            <p>更新时间:{date[0]}
              <br />白天的天气是{day_weather[0]}
              <img src="cid:img1" width="32" height="32" />晚上的天气是{night_weather[0]}
              <img src="cid:img2" width="32" height="32" />
              <br />当天日出时间:{sunrise[0]} 日落时间:{sunset[0]}
              <br />当天最高气温{temperature_max[0]}℃ 最低气温{temperature_min[0]}℃
              <br />周围空气湿度{humidity[0]}%
              <br />
              <br />==================================</p>
            </div>
            <div style="text-align: center;">
              <h2>{date[1]} 天气(预测)</h2>
              <p>白天的天气是 {day_weather[1]}
                <img src="cid:img3" width="32" height="32" />晚上的天气是 {night_weather[1]}
                <img src="cid:img4" width="32" height="32" />
                <br />当天日出时间:{sunrise[1]} 日落时间:{sunset[1]}
                <br />当天最高气温{temperature_max[1]}℃ 最低气温{temperature_min[0]}℃
                <br />周围空气湿度{humidity[1]}%
                <br /></p>
             </div>
            <div style="text-align: center;">
              <h2>{date[2]} 天气(预测)</h2>
              <p>白天的天气是{day_weather[2]}
                <img src="cid:img5" width="32" height="32" />晚上的天气是 {night_weather[2]}
                <img src="cid:img6" width="32" height="32" />
                <br />当天日出时间:{sunrise[2]} 日落时间:{sunset[2]}
                <br />当天最高气温{temperature_max[2]}℃ 最低气温{temperature_min[2]}℃
                <br />周围空气湿度{humidity[2]}% <br /> </p> </div> <div style="text-align: center; font-size: medium;"> 
                <b> <a href="https://dev.qweather.com/" style="color: black;" target="_blank"> <img 
                src="https://dev.qweather.com/assets/images/logo-s-dark.png" alt="QWeatherIcon" width="15" 
                height="15" />和风天气开发平台</a> <br /> <a href="https://github.com/MarkusJoe/HeWeatherReporter" 
                style="color: black;" target="_blank"> <img 
                src="https://gitee.com/rtakland/prefile-repo/raw/master/githubicon.png" alt="githubIcon" width="15" 
                height="15" />Github仓库</a> </b> </div> <audio controls src=""></audio> </body> 
        
        </html>
        """
        self.message['Subject'] = '3天天气预报'
        self.message.attach(MIMEText(mail_html, 'html', 'utf-8'))

        image_count = 1
        for image_source_free in icon_lst:
            with open(f'./assets/{self.icon_style}/{image_source_free}.png', 'rb') as file:
                MyImage = MIMEImage(file.read())
            MyImage.add_header('Content-ID', f'img{image_count}')
            self.message.attach(MyImage)
            image_count += 1

        try:
            self.smtp.login(self.sender, self.password)
            self.smtp.sendmail(self.sender, self.receiver, self.message.as_string())
        except smtplib.SMTPException as e:
            print(f'{Other().log_time}邮件发送错误', e)

    # 获取自然灾害
    def warning_send_mail(self):
        """

        releaseTime: 更新时间(并不是获取数据的时间 而是API更新数据的时间)
        title: 标题
        startTime: 开始时间
        endTime: 结束时间
        status: 状态
        level: 等级
        type: 类型
        text: 详细描述
        获取自然灾害并判断灾害信息是否为空
        如果空则跳过
        如果不为空则单独发送一封邮件
        :return:
        """
        API_url = f'https://devapi.qweather.com/v7/warning/now?location={self.location}&key={self.key}'
        r = requests.get(API_url, headers={'Accept-Encoding': 'gzip'}).text
        data = json.loads(r)
        returnCode_warning = data['code']
        print(f'{Other().log_time}自然灾害API请求结果:{self.codes[returnCode_warning]}')
        if data['warning']:
            public_time = data['warning'][0]['pubTime']
            title = data['warning'][0]['title']
            start_time = data['warning'][0]['startTime']
            end_time = data['warning'][0]['endTime']
            if not start_time:
                start_time = None
            elif not end_time:
                end_time = None
            status = data['warning'][0]['status']
            if status == 'update':
                status = '[预警更新]'
                print(f'{Other().log_time}预警信息已更新')
            elif status == 'active':
                status = '[新的预警]'
                print(f'{Other().log_time}获取到新的灾害预警')
            elif status == 'cancel':
                print(f'{Other().log_time}预警已取消')

            level = data['warning'][0]['level']
            type_ = data['warning'][0]['type']
            type_ = type_name[type_]
            text = data['warning'][0]['text']
            self.message['Subject'] = '自然灾害预警'
            self.message['Subject'] = f'{title}'
            mail_html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Warning</title>
            </head>
            <body>
            <div style="text-align: center;color: black;">
                <h2>{title}</h2>
                <h3>预警发布时间:{public_time[:10]} {level}预警</h3>
                <p>
                    预警状态:{status} 预警类型:{type_} 持续时间:{start_time[:10]}-{end_time[:10]}
                    <br />
                    {text}
                </p>
            </div>
            
            </body>
            </html>
            """
            self.msg_content.attach(MIMEText(mail_html, 'html', 'utf-8'))
            self.message.attach(self.msg_content)
            try:
                if status != 'cancel':
                    self.smtp.login(self.sender, self.password)
                    self.smtp.sendmail(self.sender, self.receiver, self.message.as_string())
            except smtplib.SMTPException as e:
                print(f'{Other().log_time}邮件发送错误', e)


class Other:
    def __init__(self):
        self.log_time = time.strftime("[%H:%M:%S]", time.localtime())

    def run(self, run_mode, times):
        """

        循环检测时间如果本地时间等于配置文件内填写的时间则发送一封天气信息的邮件
        :return:
        """
        if run_mode == 'dev':
            while True:
                time_local = time.strftime("%H:%M", time.localtime())
                print(f'self.log_time运行中  发送模式: Dev 发送时间:{times}')
                if time_local in times:
                    SendWeatherMail().Dev_mode()
                    print(f'{self.log_time}正在发送邮件...')
                    time.sleep(61)
        elif run_mode == 'free':
            while True:
                time_local = time.strftime("%H:%M", time.localtime())
                print(f'{self.log_time}运行中  发送模式: Dev 发送时间:{times}')
                if time_local in times:
                    SendWeatherMail().Free_mode()
                    print(f'{self.log_time}正在发送邮件...')
                    time.sleep(61)

    def check_config(self):
        for mail in my_config['mail-settings'].values():
            if mail is None:
                print(f'{self.log_time}[ERROR]"mail-settings"有未填写项...')
                sys.exit(1)
        for request in my_config['request-settings'].values():
            if request is None:
                print(f'{self.log_time}[ERROR]"request-settings"有未填写项...')
                sys.exit(1)
        for other in my_config['other-settings'].values():
            if other is None:
                print(f'{self.log_time}[ERROR]"request-settings"有未填写项...')
                sys.exit(1)


if __name__ == '__main__':
    yaml = YAML()
    my_config_file = 'config.yml'

    print(f'{Other().log_time}请不要在配置文件中随意添加字符\n')
    with open(my_config_file, 'r', encoding='utf-8') as f:
        my_config = yaml.load(f)

    Other().check_config()
    icon_style = my_config['other-settings']['icon-style']

    if icon_style not in ['set-1-bw', 'set-1-color', 'set-2', 'random']:
        print(f'{Other().log_time}[ERROR]图标文件错误请检查配置文件填写是否正确...')
        sys.exit(1)
    elif icon_style == 'random':
        styles = ['set-1-bw', 'set-1-color', 'set-2']
        icon_style = random.choice(styles)

    # 自然灾害中的typeID 对应的类型
    with open('assets/resources/type_warning.json', 'r', encoding='utf-8') as f:
        type_name = json.loads(f.read())
    # 获取命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', help='Some operations for test.',
                        choices=['free', 'dev', 'warning', 'war-force'])
    arg_test = parser.parse_args().test
    if arg_test:
        if arg_test == 'dev':
            SendWeatherMail().Dev_mode()
            print(f'{Other().log_time}执行完成...')
            sys.exit(0)
        elif arg_test == 'free':
            SendWeatherMail().Free_mode()
            print(f'{Other().log_time}执行完成...')
            sys.exit(0)
        elif arg_test == 'warning':
            SendWeatherMail().warning_send_mail()
            print(f'{Other().log_time}执行完成...')
            sys.exit(0)
        elif arg_test == 'war-force':
            SendWeatherMail().warning_send_mail()
            print(f'{Other().log_time}执行完成...')
            sys.exit(0)

    send_time = my_config['other-settings']['send-times']
    # 使用多进程来实现发送正常天气和每10分钟一次的检查自然灾害预报
    Process(target=Other.run, args=(my_config['request-settings']['mode'], send_time,)).start()

    # 启动时检查一次
    SendWeatherMail().warning_send_mail()

    # 每10分钟检查一次自然灾害预报 在运行程序的时候也会检查一次
    time_count = 0
    while True:
        time.sleep(1)
        time_count += 1
        if time_count == 600:
            SendWeatherMail().warning_send_mail()
            time_count = 0
