from flask import Blueprint, request

from services import templates as templates_service
from utils.request import validate_body
from utils.response import response, error_response

templates = Blueprint('templates', __name__)


@templates.route('/', methods=['POST'])
def create_template():
    body = request.get_json()
    status, missing_field = validate_body(body, ['message'])
    if not status:
        return error_response(f'{missing_field} is required')

    try:
        templates_service.create_template(body)
        return response(True, 'Template created successfully', body)
    except Exception as err:
        print('=====> Error', err)
        return error_response(str(err))


@templates.route('/<template_id>')
def view_one(template_id):
    try:
        data = templates_service.get_template(template_id)
        return response(True, 'Template', data)
    except Exception as err:
        print('=====> Error', err)
        return error_response(str(err))


@templates.route('/<template_id>', methods=['PUT'])
def update(template_id):
    body = request.get_json()
    status, missing_field = validate_body(body, ['message'])
    if not status:
        return error_response(f'{missing_field} is required')

    try:
        template = templates_service.update_template(template_id, body)
        return response(True, 'Template created successfully', template)
    except Exception as err:
        print('=====> Error', err)
        return error_response(str(err))


@templates.route('/<template_id>', methods=['DELETE'])
def delete(template_id):
    try:
        templates_service.delete_template(template_id)
        return response(True, 'Templated Deleted', None)
    except Exception as err:
        print('=====> Error', err)
        return error_response(str(err))
