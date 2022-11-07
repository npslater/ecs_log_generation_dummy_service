import json
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def default():
    return {'status': 'alive'}, 200, {'ContentType': 'application/json'}

@app.route("/dummy")
def dummy():
    payload = {
        'message': 'test'
    }
    return json.dumps(payload), 200, {'ContentType': 'application/json'}

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(debug=True, host='0.0.0.0', port=port)