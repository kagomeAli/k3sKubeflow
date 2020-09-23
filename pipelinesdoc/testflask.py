import json
import requests
from flask import Flask, request
from flask_cors import *
import time

app = Flask(__name__)

@app.route("/")
@cross_origin()
def index():
    data = request.args.get("id")
    result = {
        'status': "400",
        'data': 'error',
    }
    if data == 'aoi!)^)':
       result = {
               'status': "200",
               'data': 'success',
           }
    return json.dumps(result)

if __name__ == '__main__':
  app.run()