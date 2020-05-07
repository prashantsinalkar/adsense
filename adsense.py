from config import *
import flask
from flask import send_file
from flask import Flask, url_for, jsonify, request, redirect
import json
import os
import os.path
import base64
import re
from csv import DictWriter
import time
from os.path import abspath, dirname, exists, isfile, join, splitext
import config


current_time = time.strftime("%H:%M:%S", time.localtime())

if not os.path.exists(ADSENCE_DIR):
    os.makedirs(ADSENCE_DIR)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    refrer_url = request.referrer
    ref = request.args.get('ref')
    adcode = request.args.get('adcode')
    print(request.headers)
    print(ref)
    print(adcode)
    print("redirected to ", ref)
    remote_addr = request.remote_addr
    create_csv_log(adcode, refrer_url, ref, remote_addr)
    return redirect(ref, code=302)


def create_csv_log(adcode, refrer_url, ref, remote_addr):
    field_names = [
        'adcode',
        'refrer_url',
        'redirected_to',
        'remote_ip_address',
        'time']
    dict_of_elem = {'adcode': adcode, 'refrer_url': refrer_url,
                    'redirected_to': ref, 'remote_ip_address': remote_addr,
                    'time': current_time}
    file_name = ADSENCE_DIR + '/' + time.strftime("%Y%m%d") + '.csv'
    append_dict_as_row(file_name, dict_of_elem, field_names)


def append_dict_as_row(file_name, dict_of_elem, field_names):

    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        # Add dictionary as wor in the csv
        dict_writer.writerow(dict_of_elem)


if __name__ == '__main__':
    if (PRODUCTION):
        app.run(debug=False)
    else:
        app.run(debug=True)

    app.run(port=HTTP_PORT, host=HTTP_HOST)
