import json
from flask import Flask, request
import flask as fl
import os
import logging
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

@app.route("/")
def default():
    return healthcheck()

@app.route("/healthcheck")
def healthcheck():
    payload = {
        'message': 'test'
    }
    app.logger.debug(payload)
    return payload, 200, {'ContentType': 'application/json'}

@app.route("/item/save", methods=['GET','POST'])
def save():
    app.logger.info(json.loads(request.data))
    fl.abort(400)

@app.route("/settings/profile", methods=['GET','POST'])
def settings():
    app.logger.error(json.loads(request.data))
    fl.abort(403)

@app.route("/item/update", methods=['GET','POST'])
def update():
    app.logger.error(json.loads(request.data))
    fl.abort(500)

@app.route("/record/save", methods=['POST'])
def copycat():
    if not request.data:
        save();
    payload = json.loads(request.data)
    payload['newKey'] = 'added this key'
    app.logger.info(payload)
    return payload, 200, {'ContentType': 'application/json'}

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(debug=True, host='0.0.0.0', port=port)