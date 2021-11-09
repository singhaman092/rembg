#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import argparse
import glob
import os
from io import BytesIO
from urllib.parse import quote, unquote_plus
from urllib.request import urlopen

from flask import Flask, request, send_file
from waitress import serve

from src.rembg.bg import remove, get_model

app = Flask(__name__)


available_models = ['u2net', 'u2netp', 'u2net_human_seg']

# for m in available_models:
#     get_model(m)

# def lambda_handler(event, context):

# @app.route("/test", methods=["POST","GET"])
def handler(event,context):
    print(event)
    file_content = ''
    if event.httpMethod == 'POST':
        if 'file' not in request.files:
            return ({'error': "missing post form param 'file'"}, 400)

        file_content = request.files['file'].read()
        print(file_content)

    if event.httpMethod == 'GET':
        url = event.queryStringParameters.get("url")
        if url is None:
            return ({'error': "missing query param 'url'"}, 400)

        url = unquote_plus(url)
        if ' ' in url:
            url = quote(url, safe='/:')

        file_content = urlopen(url).read()

    if file_content == '':
        return ({'error': 'File content is empty'}, 400)

    alpha_matting = 'a' in request.values
    af = request.values.get('af', type=int, default=240)
    ab = request.values.get('ab', type=int, default=10)
    ae = request.values.get('ae', type=int, default=10)
    az = request.values.get('az', type=int, default=1000)

    model = request.args.get('model', type=str, default='u2net')

    if not model in available_models:
        app.logger.error("{} model not supported".format(model), exc_info=True)
        return ({'error': 'model not present'}, 400)

    # model_choices = [os.path.splitext(os.path.basename(x))[0] for x in
    #              set(glob.glob(model_path + '/*'))]
    # model_choices = list(set(model_choices + available_models))
    # model_path = os.environ.get('U2NETP_PATH',
    #                             os.path.expanduser(os.path.join('~',
    #                                                             '.u2net')))

    try:
        return send_file(BytesIO(remove(
            file_content,
            model_name=model,
            alpha_matting=alpha_matting,
            alpha_matting_foreground_threshold=af,
            alpha_matting_background_threshold=ab,
            alpha_matting_erode_structure_size=ae,
            alpha_matting_base_size=az,
        )), mimetype='image/png')
    except Exception as e:
        app.logger.exception(e, exc_info=True)
        return ({'error': 'oops, something went wrong!'}, 500)


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument('-a', '--addr', default='0.0.0.0', type=str,
                    help='The IP address to bind to.')

    ap.add_argument('-p', '--port', default=5000, type=int,
                    help='The port to bind to.')

    args = ap.parse_args()
    print("starting.....")
    # serve(app, host=args.addr, port=args.port)
    app.run(host='0.0.0.0', port=5000)
    print("started!")


if __name__ == '__main__':
    main()
