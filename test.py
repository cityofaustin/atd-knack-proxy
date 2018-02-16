'''
Test your esb-knack webserver
'''
import requests
from secrets import KNACK_CREDS

app_id = KNACK_CREDS['test']['app_id']
api_key = KNACK_CREDS['test']['api_key']

#  specify the destination object in your knack app
obj_key = 'object_83'

port = '5002'
endpoint = f'http://localhost:{port}/objects/{obj_key}/records'

#  match your object's schema
record = {
    "field_1447":"2018-000000000000046888",
    "field_1448":"430978528",
    "field_1232":"18-99443972"
}

headers = {
    'x-knack-application-id': app_id,
    'x-knack-rest-api-key': api_key,
}

res = requests.put(
    insert_endpoint,
    headers=headers,
    data=record_dict,
    # verify='cert.pem' #  for ssl, must specify an https endpoint and deploy certs on webserver 
)

res.raise_for_stats()

print(res.json())

