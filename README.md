# WeatherSystem
# 使用前准备
请务必从Releases中下载
### 本程序基于Python 3.x 以及[和风天气API](https://dev.qweather.com/)
- 请现在电脑上安装python 3.x版
- 首先在路径栏中输入 `pip -r requirements.txt` 等待安装完成后打开Config.yaml 修改内容 配置文件中的所有项必须全部填写且正确
#### China-City-List.txt来自[和风天气LocationID](https://github.com/qwd/LocationList) 内容稍作修改
以下是各个参数代表的意义

Config.yaml
- `key`:  API的密钥 获取请前往[创建应用和KEY](https://dev.qweather.com/docs/start/get-key/) 创建过程请选择WebAPI
- `mode`: 发送模式
- `location`:  获取数据的城市 运行SearchCity.py进行自助搜索
- `sender`:  发送邮件的账号
- `password`:  发送邮件账号的登录密钥
- `receiver`:  接收邮件的账号
- `server`:  发送邮件的中转服务器
- `port`:  服务器端口
- `time`:  发送时间

 # 运行程序
双击Weather.py
