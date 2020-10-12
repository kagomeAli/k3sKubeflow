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
    pipename = request.args.get("pipename")
    pipeid = request.args.get("pipeid")
    result = {
        'status': "400",
        'data': 'error',
    }
    print('接收请求')
    if data == 'aoi!)^)':
        ticks = time.time()
        print('当前时间戳： ', ticks)
        new_ticks = pipename + str(ticks).replace('.', '')
        print(new_ticks)
        result = client.run_pipeline(experiment_id='663212b7-12c9-430c-92ff-25d1bdc26ccf',job_name=new_ticks, pipeline_id=pipeid,version_id=pipeid)
        print(result)
        result = {
           'status': "200",
           'data': 'success',
        }
    return json.dumps(result)


@app.route("/getList",methods=["GET"])
@cross_origin()
def check():
    return_dict= {'return_code': '200', 'return_info': '处理成功', 'result': False}
    result = client.list_pipelines().to_dict()
    return result


# http://0.0.0.0:8882/getList
if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8882,debug=True)
