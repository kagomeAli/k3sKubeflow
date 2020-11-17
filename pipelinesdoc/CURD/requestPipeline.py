import json
from flask import Flask, request
from flask_cors import *
import datetime
import time
import kfp
import kfp.dsl as dsl
import os
import zipfile

config = {
    #身份驗證ID
    "id"：'aoi!)^)',
    # pipeline運行後所在erperiment id
    "experiment_id"："663212b7-12c9-430c-92ff-25d1bdc26ccf",
    #解壓的pipeline的ID
    "unzip_pipeid"："0a81b7a0-d0cf-4923-9725-dbbd7b3635b0"
}

client = kfp.Client()
app = Flask(__name__)

@app.route("/")
@cross_origin()
def index():
    # result = client.list_experiments()
    # client.list_pipelines()
    # pipelineLab.py.yaml
    #client.run_pipeline(config["experiment_id"],job_name='fabricModel2', pipeline_package_path='./pipelineLab.py.yaml')
    data = request.args.get("id")
    pipename = request.args.get("pipename")
    pipeid = request.args.get("pipeid")
    result = {
        'status': "400",
        'data': 'error',
    }
    print('接收请求')
    if data == config['id']:
        ticks = time.time()
        print('当前时间戳： ', ticks)
        new_ticks = pipename + str(ticks).replace('.', '')
        print(new_ticks)
        result = client.run_pipeline(config["experiment_id"],job_name=new_ticks, pipeline_id=pipeid,version_id=pipeid)
        print(result)
        result = {
           'status': "200",
           'data': 'success',
        }
    return json.dumps(result)


@app.route("/getlist")
@cross_origin()
def getlist():
    return_dict= {'return_code': '200', 'return_info': '处理成功', 'result': False}
    result = client.list_pipelines().to_dict()
    return result

@app.route("/allexp")
@cross_origin()
def allexp():
    # result = client.list_experiments().to_dict()
    # result = client.list_runs(experiment_id='75c0dab5-1b11-4544-9638-8129928bc35e').to_dict()
    # result = client.list_runs(sort_by='created_at', page_size=2, experiment_id=config["experiment_id"]).to_dict()
    length = client.list_runs(page_size=1, experiment_id=config["experiment_id"]).to_dict()['total_size']
    data = client.list_runs(page_size=length, experiment_id=config["experiment_id"]).to_dict()['runs']
    data.reverse()
    result = {'pipelines': data }
    return result

@app.route("/unzip")
@cross_origin()
def unzip():
    result= {'status': '200', 'result': False}
    ticks = time.time()
    new_ticks = 'unzip_' + str(ticks).replace('.', '')
    data = client.run_pipeline(config["experiment_id"],job_name=new_ticks, pipeline_id=config["unzip_pipeid"],version_id=config["unzip_pipeid"])
    data = client.run_pipeline(config["experiment_id"],job_name=new_ticks, pipeline_id=config["unzip_pipeid"],version_id=config["unzip_pipeid"])
    print(data)
    return result

#curl http://127.0.0.1:30082/allexp
if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8882,debug=True)
