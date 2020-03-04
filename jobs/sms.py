from multiprocessing import Queue

from services.audience import message_audience
from services.templates import get_template

sms_queue = Queue()


def sms_job():
    while True:
        if sms_queue.empty():
            continue
        data = sms_queue.get()
        template = get_template(data['template_id'])
        message_audience(data['audience_id'], template, data['args'])
        print(f'=====> Successfully messaged {data["audience_id"]} with template {data["template_id"]}')