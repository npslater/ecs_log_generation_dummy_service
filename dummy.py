import json
from flask import Flask, request
import flask as fl
import os
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
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
app.logger.setLevel('DEBUG')

@app.route("/")
def default():
    return {'status': 'alive'}, 200, {'ContentType': 'application/json'}

@app.route("/dummy")
def dummy():
    payload = {
        'message': 'test'
    }
    app.logger.debug(payload)
    return payload, 200, {'ContentType': 'application/json'}

@app.route("/badrequest", methods=['GET','POST'])
def badrequest():
    app.logger.error(json.loads(request.data))
    fl.abort(400)

@app.route("/nopermission", methods=['GET','POST'])
def nopermission():
    app.logger.error(json.loads(request.data))
    fl.abort(403)

@app.route("/internalerror", methods=['GET','POST'])
def internalerror():
    app.logger.error(json.loads(request.data))
    fl.abort(500)

@app.route("/copycat", methods=['POST'])
def copycat():
    if not request.data:
        badrequest();
    payload = json.loads(request.data)
    payload['newKey'] = 'copycat added this key'
    app.logger.info(payload)
    return payload, 200, {'ContentType': 'application/json'}

@app.route("/status/<code>")
def status(code):
    statusCode = int(code)
    app.logger.info(statusCode)
    if code != 200:
        fl.abort(statusCode)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(debug=True, host='0.0.0.0', port=port)