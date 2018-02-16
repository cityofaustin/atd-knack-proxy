'''
A Restful API interface to the Knack API
Because sometimes legacy applications require goofy shit like this

See: https://www.knack.com/developer-documentation/#the-api
!!! Only supports record create (POST)

'''
import datetime
import logging
from logging.handlers import RotatingFileHandler
import json
import pdb

from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
import requests
from secrets import SECRET_KEY

app = Flask(__name__)
api = Api(app)

app.secret_key = SECRET_KEY
parser = reqparse.RequestParser()
parser.add_argument('x-knack-application-id', location='headers')
parser.add_argument('x-knack-rest-api-key', location='headers')


class Record(Resource):
    '''
    Define REST endpoint
    '''
    def post(self, obj_key):
        app.logger.info(str(datetime.datetime.now()))
        app.logger.info(request.url)
        
        data = request.get_json()
        app.logger.info(request.is_json)
        
        app.logger.info(data)
        args = parser.parse_args()
        app.logger.info(args)

        res = create_record(data, obj_key, args)
        return res.text


def handle_response(res):
    '''
    Check Knack API response for errors and abort request as needed
    '''
    if res.status_code == 200:
        return res
    else:
        app.logger.info(res.status_code)
        app.logger.info(res.text)
        abort(res.status_code, message=res.text)


def create_record(payload, obj_key, headers, max_attempts=5, timeout=10): 
    '''
    Submit a POST request to create a Knack record
    '''
    headers['Content-type'] = 'application/json' #  require by knack like so
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
            
            break

        except requests.exceptions.Timeout as e:

            if attempts < max_attempts:
                continue
            else:
                raise e

    handle_response(res)
    return res


api.add_resource(Record, '/objects/<string:obj_key>/records')


if __name__ == '__main__':
    handler = RotatingFileHandler('log/app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    # SSL Support
    # app.run(debug=False,host='0.0.0.0',port=5002, ssl_context=('cert.pem', 'key.pem'))
    app.run(debug=True,host='0.0.0.0',port=5002)


