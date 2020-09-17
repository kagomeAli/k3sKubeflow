import json
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    result = {
        'status': "200",
        'data': 'Hello, world!',
    }
    return json.dumps(result)

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8802,debug=True)
