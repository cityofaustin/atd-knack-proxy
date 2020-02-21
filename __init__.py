"""
Restful API interface to the Knack API

See: https://www.knack.com/developer-documentation/#the-api
"""
import datetime

from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
import requests

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("x-knack-application-id", location="headers")
parser.add_argument("x-knack-rest-api-key", location="headers")

class Record(Resource):
    """
    Define REST endpoint
    """

    def post(self, obj_key):
        app.logger.info(str(datetime.datetime.now()))
        app.logger.info(request.url)

        data = request.get_json()
        app.logger.info(request.is_json)

        app.logger.info(data)
        args = parser.parse_args()
        if args.get("x-knack-application-id") == "5d13ae5b438091000ac0197d":
            abort(502, message="This service is unavailable until 6pm CT on 21 Feb 2020.")
            
        app.logger.info(args)

        res = create_record(data, obj_key, args)
        return res.json()


def handle_response(res):
    """
    Check Knack API response for errors and abort request as needed
    """
    if res.status_code == 200:
        return res
    else:
        app.logger.info(res.status_code)
        app.logger.info(res.text)
        abort(res.status_code, message=res.text)


def create_record(payload, obj_key, headers, max_attempts=5, timeout=30):
    """
    Submit a POST request to create a Knack record
    """
    headers["Content-type"] = "application/json"  #  required by knack like so
    endpoint = "https://api.knack.com/v1/objects/{}/records".format(obj_key)

    attempts = 0

    while attempts < max_attempts:

        attempts += 1

        try:
            res = requests.post(
                endpoint, headers=headers, json=payload, timeout=timeout
            )

            break

        except requests.exceptions.Timeout as e:

            if attempts < max_attempts:
                continue
            else:
                raise e

    handle_response(res)
    return res


api.add_resource(Record, "/v1/objects/<string:obj_key>/records")


@app.route("/")
def health_check():
    now = datetime.datetime.now()
    return (
        "Knack Proxy - Health Check - Available @ %s"
        % now.strftime("%Y-%m-%d %H:%M:%S"),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True)
