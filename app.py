from flask import Flask, request
from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()

from utils.request import validate_body
from utils.response import response, error_response
from utils.sms import send_bulk_sms

app = Flask(__name__)

CORS(app)


@app.route('/message', methods=['POST'])
def message_audience():
    body = request.get_json()
    status, missing_field = validate_body(body, ['message', 'phones'])
    if not status:
        return error_response(f'{missing_field} is missing')
    send_bulk_sms(body['phones'], body['message'])
    return response(True, 'Success', None)


if __name__ == '__main__':
    app.run()