# 声明
- *程序作者: **RTAkland (markushammered@gmail.com)***
- 和风天气开发者平台：<i><a href="https://dev.qweather.com" target="_blank">和风天气开发者平台</a></i>
- 和风天气官网: <i><a href="https://qweather.com" target="_blank">和风天气官网</a></i>

# 如何使用
- 程序基于python3.x开发 务必使用python3.x版本运行
- 将config.yml正确填写完成
- 使用`pip install -r requirements.txt` 安装需要的库
- 双击`Weather.py` 或 `Weather.sh`

## 推送天气信息到QQ
- 已在`module`文件夹中添加拓展　但并未添加到`Weather.py`中　可以手动运行`EXTRA_qq_pusher.py`使用
- 如何使用: 在解释器或终端中运行程序　初次运行会生成一个二维码 扫码登录即可
- 已知问题: 使用了`pcqq`库　似乎这个库只能被动发送消息　正在看源码努力解决问题中
- 已知问题: 不能使用qq账号密码登录只能通过扫码登录　但是登陆一次后会保存token使下一次运行不需要再次扫码登录
- 已知问题: 这个库用装饰器来运行相关函数　但是不同装饰器会被同一个条件触发

# English README.md
# Introduction
- Developed by **RTAkland (markushammered@gmail.com)**
- The weather API from QWeather<i><a href="https://qweather.com" target="_blank">QWeather Official Website</a></i>
- QWeather Development Platform: <i><a href="https://dev.qweather.com" target="_blank">和风天气开发者平台</a></i>

# How to use
- Run program using Python3
- Fill in the configuration file correctly
- Use `pip/pip3 -install -r requirements.txt` to install required libraries
- Run `Weather.py` or `Weather.sh`

## Push weather information to QQ
- Get into `module` and run`EXTRA_qq_pusher.py`
- If you run this for first time, you just open `QQ Mobile` and scan the `QR Code`
- Each subsequent run will automatically log in