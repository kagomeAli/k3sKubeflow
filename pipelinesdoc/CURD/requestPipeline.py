import json
from flask import Flask, request
from flask_cors import *

import time
import kfp
import kfp.dsl as dsl

client = kfp.Client()
app = Flask(__name__)

@app.route("/")
@cross_origin()
def index():
    # result = client.list_experiments()
    # client.list_pipelines()
    # pipelineLab.py.yaml
    #client.run_pipeline(experiment_id='663212b7-12c9-430c-92ff-25d1bdc26ccf',job_name='fabricModel2', pipeline_package_path='./pipelineLab.py.yaml')
    data = request.args.get("id")
    result = {
        'status': "400",
        'data': 'error',
    }
    print('接收请求')
    if data == 'aoi!)^)':
        ticks = time.time()
        print('当前时间戳： ', ticks)
        new_ticks ='fabricModel_' + str(ticks).replace('.', '')
        print(new_ticks)
        result = client.run_pipeline(experiment_id='663212b7-12c9-430c-92ff-25d1bdc26ccf',job_name=new_ticks, pipeline_id='8c049ab8-7bed-4ff0-af1a-8927770ff0c1',version_id='8c049ab8-7bed-4ff0-af1a-8927770ff0c1')
        print(result)
        result = {
           'status': "200",
           'data': 'success',
        }
    return json.dumps(result)

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8882,debug=True)
