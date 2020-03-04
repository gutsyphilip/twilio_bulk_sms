from flask import Blueprint, request

from jobs.sms import sms_queue
from services import audience as audience_service
from utils.request import validate_body
from utils.response import response, error_response

audience = Blueprint('audience', __name__)


@audience.route('/', methods=['POST'])
def create_audience():
    body = request.get_json()
    status, missing_field = validate_body(body, ['name', 'users'])
    if not status:
        return error_response(f'{missing_field} is required')
    try:
        audience_service.create_audience(body)
        return response(True, 'Success', body)
    except Exception as err:
        print('=====> Error', err)
        return error_response(str(err))


@audience.route('/<audience_id>')
def view_one(audience_id):
    try:
        data = audience_service.view_audience(audience_id)
        return response(True, 'Success', data)
    except Exception as err:
        print('=====> Error', err)
        return error_response(str(err))


@audience.route('/<audience_id>', methods=['PUT'])
def update_audience(audience_id):
    body = request.get_json()
    try:
        data = audience_service.update_audience(audience_id, body)
        return response(True, 'Success', data)
    except Exception as err:
        print('=====> Error', err)
        return error_response(str(err))


@audience.route('/message', methods=['POST'])
def message_audience():
    body = request.get_json()
    status, missing_field = validate_body(body, ['audience_id', 'template_id', 'args'])
    if not status:
        return error_response(f'{missing_field} is missing')
    sms_queue.put(body)
    return response(True, 'Success', None)


@audience.route('/<audience_id>/user', methods=['PUT'])
def add_user_to_audience(audience_id):
    body = request.get_json()
    status, missing_field = validate_body(body, ['name', 'phone'])
    if not status:
        return error_response(f'{missing_field} is missing')
    try:
        data = audience_service.add_to_audience(audience_id, body)
        return response(True, 'Success', data)
    except Exception as err:
        print('=====> Error', err)
        return error_response(str(err))


@audience.route('/<audience_id>/user', methods=['DELETE'])
def delete_user_from_audience(audience_id):
    phone = request.args.get('phone')
    if not phone:
        return error_response('phone is required in query params')
    try:
        audience_service.delete_from_audience(audience_id, phone)
        return response(True, 'Success', None)
    except Exception as err:
        print('=====> Error', err)
        return error_response(str(err))


@audience.route('/<audience_id>', methods=['DELETE'])
def delete_audience(audience_id):
    try:
        audience_service.delete_audience(audience_id)
        return response(True, 'Success', None)
    except Exception as err:
        print('=====> Error', err)
        return error_response(str(err))
