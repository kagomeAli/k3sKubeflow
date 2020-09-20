import json
from flask import Flask
from flask_cors import *

import json
import kfp
import kfp.dsl as dsl

client = kfp.Client()
app = Flask(__name__)

@app.route("/")
def index():

    result = client.list_experiments()
    print(result)

    result = {
        'status': "200",
        'data': 'Hello, world!',
    }
    return json.dumps(result)

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8882,debug=True)
