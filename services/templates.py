from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient('mongodb://localhost/')

templates = client['twilio']['templates']


def create_template(data):
    templates.insert_one(data)


def get_template(template_id):
    result = templates.find_one({'_id': ObjectId(template_id)})
    return dict(result) if result else None


def update_template(template_id, data):
    template = templates.find_one_and_update({'_id': ObjectId(template_id)}, {'$set': data}, return_document=True)
    return template


def delete_template(template_id):
    templates.find_one_and_delete({'_id': ObjectId(template_id)})
