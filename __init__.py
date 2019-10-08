'''
Restful API interface to the Knack API

See: https://www.knack.com/developer-documentation/#the-api
'''
import datetime
import logging
from logging.handlers import RotatingFileHandler
import json
import time
import pdb

from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
import requests

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('x-knack-application-id', location='headers')
parser.add_argument('x-knack-rest-api-key', location='headers')


class Record(Resource):
    '''
    Define POST endpoint
    '''
    def post(self, obj_key, max_throttle=8):
        data = request.get_json()
        
        args = parser.parse_args()

        res = create_record(data, obj_key, args)
        return res.json()


def create_record(payload, obj_key, headers, max_attempts=5, timeout=10): 
    '''
    Submit a POST request to create a Knack record
    '''
    headers['Content-type'] = 'application/json' #  required by knack like so
    endpoint = 'https://api.knack.com/v1/objects/{}/records'.format(obj_key)

    attempts = 0

    while attempts < max_attempts:
        
        attempts += 1

        try:
            res = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=timeout
            )

            if res.status_code == 200:
                break
            
            elif res.status_code == 502:
                # 502 errors are common with Knack API
                # so try again until max attempts reached
                if attempts < max_attempts:
                    # wait a sec to give the API a break
                    time.sleep(1)
                    continue
                else:
                    abort(res.status_code, message=res.text)

            else:
                abort(res.status_code, message=res.text)

        except requests.exceptions.Timeout as e:

            if attempts < max_attempts:
                continue
            else:
                raise e

    return res


api.add_resource(Record, '/v1/objects/<string:obj_key>/records')


if __name__ == '__main__':
    app.run(debug=True)
    handler = RotatingFileHandler('log/app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
