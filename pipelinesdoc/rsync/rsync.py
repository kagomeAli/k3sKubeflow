import paramiko
import sys
import os


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

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(host, port, username, password)
    scpclient = SCPClient(ssh_client.get_transport(),socket_timeout=15.0)
    local_dir = '/mnt/1060dir/models/fabric/'
    remote_path = '/home/nvidia/Downloads'
    file_list,dir_list = get_file_path(local_dir)
    files = os.listdir(local_dir)
    print("文件上传成功")
    ssh_client.close()

 # /mnt/1060dir/models/fabric nvidia@140.115.53.52:/home/nvidia/Downloads

if __name__ == '__main__':
    unix_ts = sys.argv[1]
    uploadFile2Remote()
