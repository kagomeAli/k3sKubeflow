#import os
#def uploadFile2Remote():
#    os.system('scp -P 21000 -r ./models/fabric nvidia@140.115.53.52:/home/nvidia/Downloads/test/')

# rsync -e "ssh -p21000" -auvz --progress --delete --bwlimit=2048 ./models/fabric nvidia@140.115.53.52:/home/nvidia/Downloads/test/

#if __name__ == '__main__':
#    uploadFile2Remote()
import paramiko
import sys
import os
from scp import SCPClient


def get_file_path(root_path,file_list=[],dir_list=[]):
    #获取该目录下所有的文件名称和目录名称
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        #获取目录或者文件的路径
        dir_file_path = os.path.join(root_path,dir_file)
        #判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            dir_list.append(dir_file_path)
            #递归获取所有文件和目录的路径
            get_file_path(dir_file_path,file_list,dir_list)
        else:
            file_list.append(dir_file_path)
    return file_list,dir_list

def uploadFile2Remote():

    host = "140.115.53.52"  #服务器ip地址
    port = 21000  # 端口号
    username = "nvidia"  # ssh 用户名
    password = "NviDia!@#$"  # 密码

    #ssh 连接
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(host, port, username, password)
    scpclient = SCPClient(ssh_client.get_transport(),socket_timeout=15.0)

    # 传输文件
    #local_dir = '/data/models/fabric/'
    local_save_models = './models/fabric/00000123/saved_model.pb'
    local_variable = './models/fabric/00000123/variables/variables.data-00000-of-00001'
    local_variable2 = './models/fabric/00000123/variables/variables.index'

    remote_save_models = '/home/nvidia/Downloads/fabric/00000123/'
    remote_variable = '/home/nvidia/Downloads/fabric/00000123/variables/'

    scpclient.put(local_save_models, remote_save_models)
    scpclient.put(local_variable, remote_variable)
    scpclient.put(local_variable2, remote_variable)
    print("文件上传成功")

    ssh_client.close()

 # /mnt/1060dir/models/fabric nvidia@140.115.53.52:/home/nvidia/Downloads

if __name__ == '__main__':
    unix_ts = sys.argv[1]
    uploadFile2Remote()
