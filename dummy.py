import json
from flask import Flask, request
import os
import logging
from waitress import serve
from paste.translogger import TransLogger
import uuid
import random

logger = logging.getLogger("waitress")
logger.setLevel(logging.INFO)
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s")

app = Flask(__name__)

@app.route("/")
def default():
    return healthcheck()

@app.route("/healthcheck")
def healthcheck():
    payload = {
        'message': 'test'
    }
    logger.debug(payload)
    return payload, 200, {'ContentType': 'application/json'}

@app.route("/item/save", methods=['GET','POST'])
def save_item():
    logger.info(json.loads(request.data))
    return {"error": "Malformed Request"}, 400, {'ContentType': 'application/json'}

@app.route("/settings/profile", methods=['GET','POST'])
def settings():
    logger.error(json.loads(request.data))
    return {"error": "Access Denied"}, 403, {'ContentType': 'application/json'}

@app.route("/item/update", methods=['POST'])
def update():
    logger.error(json.loads(request.data))
    return {"error": "Internal Server Error"}, 500, {'ContentType': 'application/json'}

@app.route("/record/save", methods=['POST'])
def save_record():
    payload = json.loads(request.data)
    if not "expiry" in payload:
        logger.error("expiry field missing: {}".format(payload))
        return {"error": "Unauthorized"}, 401, {"ContentType": "application/json"}
    payload["transactionId"] = uuid.uuid4().hex
    logger.info(payload)
    return payload, 200, {'ContentType': 'application/json'}

@app.route("/ingest", methods=["POST"])
def ingest():
    payload = json.loads(request.data);
    numThreads = 0
    if not "numThreads" in payload:
        numThreads = 1
    else:
        numThreads = payload["numThreads"]
    runningThreads = random.randint(10,100)
    logger.info("Launching {} new threads. {} total threads running".format(numThreads, runningThreads))
    payload["runningThreads"] = runningThreads
    return payload, 200, {"ContentType": "application/json"}


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    serve(TransLogger(app), host="0.0.0.0", port=port)