import json
from flask import Flask, request
from flask_cors import *
import time
import kfp
import kfp.dsl as dsl
import os
import zipfile

client = kfp.Client()
app = Flask(__name__)

@app.route("/")
@cross_origin()
def index():
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


@app.route("/getlist")
@cross_origin()
def getlist():
    return_dict= {'return_code': '200', 'return_info': '处理成功', 'result': False}
    result = client.list_pipelines().to_dict()
    return result

@app.route("/lastexp")
@cross_origin()
def lastexp():
    result = client.list_runs(page_size=1, experiment_id='663212b7-12c9-430c-92ff-25d1bdc26ccf').to_dict()['total_size']
    lastresult = result - 1
    result2 = client.list_runs(page_size=result, experiment_id='663212b7-12c9-430c-92ff-25d1bdc26ccf').to_dict()['runs'][lastresult]
    return result2

@app.route("/upzip")
@cross_origin()
def upzip():
    unzip_path = '/home/aoi1060/Downloads/fabricModel/labels/'
    zip_file_name = '/home/aoi1060/Downloads/labels-json.zip'
    result= {'status': '400', 'return_info': '文件不存在', 'result': False}
    r = zipfile.is_zipfile(zip_file_name)
    file = []
    if r:
        # 删除文件夹里的文件
        for root, dirs, files in os.walk(unzip_path):
            print(files)
            for file in files:
                os.remove(unzip_path + file)
         # 解压
        fz = zipfile.ZipFile(zip_file_name, 'r')
        for file in fz.namelist():
            fz.extract(file, unzip_path)
        # 解压后，删除压缩档案
        os.remove(zip_file_name)
        result= {'status': '200', 'return_info': '解压成功', 'result': False}
    else:
        print('This is not zip')
    return result

# http://10.43.235.160:8882/
if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8882,debug=True)
