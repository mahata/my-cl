#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, send_from_directory

import celery_tasks
import random
import string
import urllib


IMAGE_DIR = 'img'


def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


app = Flask(__name__)
app.config.from_pyfile('config_file.cfg')


@app.route('/ping')
def ping():
    return 'OK'


@app.route('/img/<path>')
def show_image(path):
    return send_from_directory(IMAGE_DIR, path)


@app.route('/api/v1/resize', methods=['POST'])
def resize_api():
    url = request.form['url']

    fetch_url = urllib.parse.unquote(url)
    output_file = f'_{random_string(8)}'
    celery_tasks.resize.delay(fetch_url, f'{IMAGE_DIR}/{output_file}')

    data = [
        {'output': f'{app.config["WEB_SERVER_URL"]}/img/{output_file}'},
    ]

    return jsonify({
        'status': 'OK',
        'data': data
    })


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
