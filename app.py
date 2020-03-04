import atexit

from flask import Flask

from controllers.audience import audience
from controllers.templates import templates
from jobs import start_sms_job, close_workers


def create_app():
    workers = start_sms_job()
    atexit.register(close_workers, workers)
    return Flask(__name__)


app = create_app()

app.register_blueprint(audience, url_prefix='/audience')
app.register_blueprint(templates, url_prefix='/templates')

if __name__ == '__main__':
    app.run()
