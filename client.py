#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------- Sensor Data Client ----------------------
import re
import sys
import requests
from requests.exceptions import ConnectionError, ReadTimeout


matrix = 99
host = 'http://192.168.1.4:8000/'

def check(data):
    """Checksum Packet
    Data Type '{[1, 3], 2}' str
    """
    try:
        check_data = re.search(r'\{\[\d+\,\s\d+],\s\d+\}', data).group()
        if check_data:
            check_xy = re.findall('\[(\d+)\,\s(\d+)\]\,\s(\d+)', check_data)[0]
            x, y, value = check_xy
            if 0 <= int(x) <= matrix and 0 <= int(y) <= matrix:
                if value not in ['1', '0']:
                    print(f'>>>Data occupancy value {value} not up par')
                    return None
                return check_xy
            else:
                print(f'>>>Data position coordinates {data} out of range')
                return None
    except AttributeError:
        print(f'>>> Packets {data}  format error')
        return None


class Explain:
    """
    >>>[At least 2 parameters are required for the execution terminal to send and receive packets]
        --Parameter 1: 1 or 2 (analogue sensor terminal, 1 for sensor client 1)
        --Parameter 2: send or receive (send client sends packet, receive client receives data)
        --Parameter 3: packet, example {[1, 3], 0}
        Example: python client.py 1 send {[1, 3], 0} means that client 1 sends a packet to the server.
    """


# Calibration parameters
if sys.argv[1] in ['1', '2']:
    if sys.argv[2] == 'send':
        try:
            result = check(sys.argv[3])
            if result:
                x, y, value = result
                data = '{' + str([int(x), int(y)]) + ',' + ' ' + value + '}'
                print('Data Format：', data)
                try:
                    print(f'>>>Client Sensor[{sys.argv[1]}]Is Attempting to send a packet to the server side')
                    res = requests.post(url=host + "collect", data={'data': data}, timeout=5)
                    print(res.text)
                except (ConnectionError, ReadTimeout):
                    print('>>>Server-side services not turned on！')
            else:
                print(Explain.__doc__)
                exit()
        except IndexError:
            print(Explain.__doc__)
            exit()

    elif sys.argv[2] == 'receive':
        try:
            print(f'>>>Client Sensors[{sys.argv[1]}]Is Attempting to receive sensor data Occupancy status')
            res1 = requests.get(url=host + "occupy", timeout=5)
            print('>>>Received data:', res1.text)
        except (ConnectionError, ReadTimeout):
            print('>>>Server-side services not turned on！')
    else:
        print(Explain.__doc__)
        exit()
else:
    print(Explain.__doc__)
    exit()