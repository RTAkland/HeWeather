#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/10/16
# @File Name: server.py

import socket

ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ListenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ListenSocket.bind(('127.0.0.1', 8000))
ListenSocket.listen(10)


def rev_msg():
    conn, addr = ListenSocket.accept()
    if "!!" in conn.recv(1024).decode('utf-8'):
        return data
    conn.close()


while True:
    msg = rev_msg()
    if msg is not None:
        data = str(msg.split()[17]).split(',')[1].split(':')[1]
        if data in ['!!tq', '!!TQ', '!!Tq', '!!tQ', '!!weather', '!!Weather']:

