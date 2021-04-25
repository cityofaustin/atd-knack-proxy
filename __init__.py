"""
Restful API interface to the Knack API

See: https://www.knack.com/developer-documentation/#the-api
"""
import datetime
import time

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
        headers = parser.parse_args()
        payload = request.get_json()

        app_id = headers.get("x-knack-application-id")
        app.logger.info(f"App ID: {app_id}")
        app.logger.info(payload)

        res = create_record(payload, obj_key, headers)
        return res.json()


def handle_failed_request(attempts, max_attempts, status_code, message):
    app.logger.info(f"Error on attempt #{attempts}: {status_code}: {message}")
    if status_code != 408 and status_code < 500:
        #  40x errors are returned by Knack when a request a fails validation. We should
        #  not should not retry when this happens
        abort(status_code, message=message)
    elif attempts < max_attempts:
        time.sleep(1)
    else:
        abort(status_code, message=message)


def create_record(payload, obj_key, headers, max_attempts=5, timeout=60):
    """
    Submit a POST request to create a Knack record.

    If 5xx error (a recurring problem with the Knack API) or timeout, retry until
    max_attempts is reached. Any other error is raised immediately.
    """
    headers["Content-type"] = "application/json"
    endpoint = f"https://api.knack.com/v1/objects/{obj_key}/records"
    attempts = 0

    while True:
        res = None
        status_code = None
        message = None
        attempts += 1
        try:
            res = requests.post(
                endpoint, headers=headers, json=payload, timeout=timeout
            )
            res.raise_for_status()
            return res

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            message = e.response.text

        except requests.exceptions.Timeout as e:
            # there is no requests.Response to parse on timeouts, so we set the
            # response info manually
            status_code = 408
            message = "Request Timeout"

        except Exception as e:
            # uknown error: abort now!
            app.logger.error(f"An unexpected error occured: {e.__repr__()}")
            abort(500, message="Internal Server Error")

        handle_failed_request(attempts, max_attempts, status_code, message)


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
