from bson.objectid import ObjectId
from pymongo import MongoClient

from jinja2 import Template

from utils.sms import send_sms

client = MongoClient('mongodb://localhost/')

audience_coll = client['twilio']['audience']


def create_audience(data):
    """
    {'name': 'AUDIENCE', 'users': [{'name':'favour', 'phone': ''0903}]}
    :param data:
    :return:
    """
    audience_coll.insert_one(data)


def view_audience(audience_id):
    result = audience_coll.find_one({'_id': ObjectId(audience_id)})
    return dict(result) if result else None


def update_audience(audience_id, data):
    audience = audience_coll.find_one_and_update({'_id': ObjectId(audience_id)}, {'$set': data}, return_document=True)
    return audience


def message_audience(audience_id, template, args):
    message = template['message']
    t = Template(message)
    text = t.render(**args)
    audience = view_audience(audience_id)
    if not audience:
        raise Exception('Invalid audience_id')
    users = audience['users']
    for user in users:
        send_sms(user['phone'], text)


def add_to_audience(audience_id, user_data):
    audience_data = audience_coll.find_one({'_id': ObjectId(audience_id)})
    data = dict(audience_data)
    users = data['users']
    users.append(user_data)
    updated_audience = update_audience(audience_id, {'users': users})
    return updated_audience


def delete_from_audience(audience_id, phone):
    audience_data = audience_coll.find_one({'_id': ObjectId(audience_id)})
    data = dict(audience_data)
    users = data['users']
    updated_users = filter(lambda user: user['phone'] != phone, users)
    updated_audience = update_audience(audience_id, {'users': updated_users})
    return updated_audience


def delete_audience(audience_id):
    audience_coll.find_one_and_delete({'_id': ObjectId(audience_id)})
