#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------- Sensor Data Collection Server ----------------------
import re
from flask import Flask, request, render_template, make_response

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Aggregation state
occupy = dict()

# Matrix size
matrix = 99


def init_occupy():
    for x in range(matrix):
        for y in range(matrix + 1):
            key = str([x, y])
            occupy[key] = '0'
    print('Sensor Initial Occupancy State Generation')


def check(data):
    """Parity Packet
    Data Type '{[1, 3], 2}' str
    """
    try:
        check_data = re.search(r'\{\[\d+\,\s\d+],\s\d+\}', data).group()
        if check_data:
            check_xy = re.findall('\[(\d+)\,\s(\d+)\]\,\s(\d+)', check_data)[0]
            x, y, value = check_xy
            if 0 <= int(x) <= matrix and 0 <= int(y) <= matrix:
                if value not in ['1', '0']:
                    print(f'>>>Data Occupancy Value {value} Not Up Par')
                    return None
                return check_xy
            else:
                print(f'>>>Data Position Coordinates {data} Out of Range')
                return None
    except AttributeError:
        print(f'>>> Packet {data} Formatting Error')
        return None


def handle_data(data):
    """Processing data format"""
    result = check(data)
    if result:
        datas = dict()
        x, y, value = result
        coordinate = str([int(x), int(y)])
        datas[coordinate] = value
        print('Received packets', datas)
        # Put into memory
        occupy.update(datas)
        return True
    else:
        return False


@app.route('/', methods=['GET'])
def index():
    app.template_folder = './'
    xy = list()
    for x_y in occupy:
        x, y = re.findall('\[(\d+)\,\s*(\d+)\]', x_y)[0]
        xy.append([[int(x), int(y)], int(occupy[x_y])])
    return render_template('matrix.html', occupy_output=xy)


@app.route('/collect', methods=['POST'])
def sensor_data():
    """Occupancy point data collection"""
    if not occupy:
        # Initial state of the sensor
        init_occupy()

    data = request.form.get('data')
    result = handle_data(data)
    if result:
        return f'Receive Packets: {data} Successes'
    else:
        return f'Receive Packets: {data}  Fail'


@app.route('/occupy', methods=['GET'])
def occupy_data():
    """Occupancy rate of aggregation"""
    occupy_output = list()
    for x_y in occupy:
        x, y = re.findall('\[(\d+)\,\s*(\d+)\]', x_y)[0]
        if occupy[x_y] == '1':
            occupy_output.append([[int(x), int(y)], int(occupy[x_y])])
    data = {'data': 'No sensor data currently occupied'}
    if occupy_output:
        data['data'] = occupy_output
        return make_response(data)
    return make_response(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

