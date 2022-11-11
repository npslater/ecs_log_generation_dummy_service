import json
from flask import Flask, request
import flask as fl
import os

app = Flask(__name__)
app.logger.setLevel('DEBUG')

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
    app.logger.error(json.loads(request.data))
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