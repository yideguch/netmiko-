#!/usr/bin/env python
# -*- coding: utf-8 -*-

from netmiko import ConnectHandler
import time

with open('commands.txt') as f:
        commands = f.read().splitlines()#1行ずつ読み込む


with open('devices.txt') as f:
        devices = f.read().splitlines()#一行ずつ読み込む

for ip in devices:
    cisco_device = {
            'device_type': 'cisco_ios_telnet',#telnet接続なら必須
            'ip': ip,
            'username': 'cisco',
            'password': 'cisco',
            'secret': 'cisco',
            }
    print('Connecting to ' + ip)
    #ssh = connection ,telnet = net_connect
    net_connect = ConnectHandler(**cisco_device)

    print('Entering enable mode ...')
    net_connect.enable()

    output = ''
    for cmd in commands:
        output += net_connect.send_command(cmd + '\n\n', delay_factor=2, strip_command=False, strip_prompt=False)
    

    prompt = net_connect.find_prompt()
    #print(prompt)
    hostname = prompt[:-1]
    #print(hostname)
    
    list = output.split('\n')
    list = list[3:]
    config = '\n'.join(list)
    #print(config)

    import datetime
    #取得した日のタイムスタンプ
    now = datetime.datetime.now()
    today = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
    file = today + '-' + hostname + '.txt'


    with open(file + '.txt', 'w') as backup:
        backup.write(config)
        print('Backup of ' + hostname + ' completed successfully')
        print('#' * 30)

    net_connect.disconnect()