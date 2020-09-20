import paramiko


#ssh nvidia@140.115.53.52 -p 21000
#  NviDia!@#$
# 创建sftp对象
transport = paramiko.Transport(('140.115.53.52', 21000))
transport.connect(username='nvidia', password='NviDia!@#$')
sftp = paramiko.SFTPClient.from_transport(transport)

# 上传
sftp.put("/home/aoi1060/Downloads/fabricModel/dockerfile", "/home/nvidia/Downloads/fabric/dockerfile")  # 将123.py 上传至服务器 /tmp下并改名为test.py

# 下载
# sftp.get("/home/svr/test.py", 'r_test.py')  # 将remove_path 下载到本地 local_path

# 关闭sftp对象连接
transport.close()



#cp -rf /home/aoi1060/Downloads/fabricModel/models/fabric/ nvidia@140.115.53.52:21000/home/nvidia/Downloads/fabric

