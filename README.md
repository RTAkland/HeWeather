# 下载文件请直接到Releases下载最新版本
## 邮箱服务器使用SSL 链接方式登录 请选择支持SSL链接的邮箱
### 本程序基于Python 3.x 以及[和风天气API](https://dev.qweather.com/)
- 请现在电脑上安装python 3.x版
- 首先在路径栏中输入 `pip -r requirements.txt` 等待安装完成后打开Config.yaml 修改内容 配置文件中的所有项必须全部填写且正确
#### China-City-List.txt来自[和风天气LocationID](https://github.com/qwd/LocationList) 内容稍作修改
以下是各个参数代表的意义

Config.yaml
- `key`:  API的密钥 获取请前往[创建应用和KEY](https://dev.qweather.com/docs/start/get-key/) 创建的API 请选择WebAPI
- `mode`: 发送模式
- `location`:  获取数据的城市 运行SearchCity.py进行自助搜索
- `sender`:  发送邮件的账号
- `password`:  发送邮件账号的登录密钥
- `receiver`:  接收邮件的账号
- `server`:  发送邮件的中转服务器
- `port`:  服务器端口
- `time`:  发送时间

 # 运行程序
 直接双击Weather.py
 使用命令行启动Weather.py 可以使用`dev`, `free`, `warning` 参数进行测试 (前提是配置文件填写正确) 具体参数:`python Weather.py -t dev/free/warning`
 
 v2.7.1版本以前可以使用`python SearchCity.py -i init`来初始化配置文件 注:在v2.7.1(21/9/27)以后代码取消了初始化配置文件的功能
