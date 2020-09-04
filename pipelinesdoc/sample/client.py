import kfp
from kfp import compiler
import kfp.dsl as dsl
import kfp.notebook
import kfp.gcp as gcp
client = kfp.Client()
from kubernetes import client as k8s_client
from kubernetes import config
config.kube_config.load_kube_config(config_file="/etc/rancher/k3s/k3s.yaml")

class validateOp(dsl.ContainerOp):
  """对文件中的数据进行验证"""
  def __init__(self, output_dir,inputFilename):
    super(validateOp, self).__init__(
      name='validate_number',
      image='yanqin/validate:v1',
      arguments = [
            '--inputFilename', inputFilename,
            '--output_dir', output_dir,
        ],
      file_outputs={
            'more': '/moreFilePath.txt',
            'less': '/lessFilePath.txt',
            })

class MoreThanZeroOp(dsl.ContainerOp):
  """handle the number more than zero"""
  def __init__(self,output_dir,data):
    super(MoreThanZeroOp, self).__init__(
      name='MoreThanZero',
      image='yanqin/morethanzero:v1',
      arguments = [
            '--output_dir',output_dir,
            '--data', data,
        ])

class LessThanZeroOp(dsl.ContainerOp):
  """handle the number less than zero"""
  def __init__(self,output_dir,data):
    super(LessThanZeroOp, self).__init__(
      name='LessThanZero',
      image='yanqin/lessthanzero:v1',
      arguments = [
            '--output_dir',output_dir,
            '--data', data,
        ])

@dsl.pipeline(
    name='Testpipelines',
    description='shows how to define dsl.Condition.'
)

def ValData():
    output_dir = '/mnt/1060dir'
    inputFilename = 'a.txt'
    validate = validateOp(output_dir,inputFilename).add_volume(k8s_client.V1Volume(name='dsl-data',host_path=k8s_client.V1HostPathVolumeSource(path='/mnt/1060dir'))).add_volume_mount(k8s_client.V1VolumeMount(mount_path='/mnt/1060dir',name='dsl-data'))
    moreThanZero = MoreThanZeroOp(output_dir,validate.outputs['more']).add_volume(k8s_client.V1Volume(name='dsl-data',host_path=k8s_client.V1HostPathVolumeSource(path='/mnt/1060dir'))).add_volume_mount(k8s_client.V1VolumeMount(mount_path='/mnt/1060dir',name='dsl-data'))
    lessThanZero = LessThanZeroOp(output_dir,validate.outputs['less']).add_volume(k8s_client.V1Volume(name='dsl-data',host_path=k8s_client.V1HostPathVolumeSource(path='/mnt/1060dir'))).add_volume_mount(k8s_client.V1VolumeMount(mount_path='/mnt/1060dir',name='dsl-data'))

compiler.Compiler().compile(ValData, 'test.yaml')