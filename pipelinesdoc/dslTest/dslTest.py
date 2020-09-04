import kfp
from kfp import compiler
import kfp.dsl as dsl

class strToList(dsl.ContainerOp):
  """将字符串转为list"""
  def __init__(self, data):
    super(strToList, self).__init__(
      name='strToList',
      image='yanqin/strtolist:v1',
      arguments = [
          '--data', data,
      ],
      file_outputs={
          'listData': 'result',
      })

def print_op(msg):
    """Print a message."""
    return dsl.ContainerOp(
        name='Print',
        image='alpine:3.6',
        command=['echo', msg],
    )

@dsl.pipeline(
    name='Testpipelines',
    description='shows how to define dsl.Condition.'
)

def ValData(inputdata, splitNum):
    listData = strToList(inputdata)
    print_op(listData.outputs['listData'])



compiler.Compiler().compile(ValData, 'test.yaml')