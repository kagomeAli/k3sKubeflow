import kfp
from kfp import compiler
import kfp.dsl as dsl

class strToList(dsl.ContainerOp):
  """将字符串转为list"""
  def __init__(self, data):
    super(strToList, self).__init__(
      name='strToList',
      image='strtolist:v1',
      arguments = [
          '--data', data,
      ],
      file_outputs={
          'listData': 'result',
      })

class validateOp(dsl.ContainerOp):
  """对文件中的数据进行验证"""
  def __init__(self,listData,number):
    super(validateOp, self).__init__(
      name='validate_number',
      image='validate:v1',
      arguments = [
            '--data', listData,
            '--deliveryNum', number
        ],
      file_outputs={
            'more': 'moreData',
            'less': 'lessData',
            })

class MoreThanZeroOp(dsl.ContainerOp):
  """handle the number more than zero"""
  def __init__(self,data):
    super(MoreThanZeroOp, self).__init__(
      name='MoreThanZero',
      image='morethanzero:v1',
      arguments = [
            '--data', data,
        ],
      file_outputs={
          'addMore': 'addData',
      })


class LessThanZeroOp(dsl.ContainerOp):
  """handle the number less than zero"""
  def __init__(self,data):
    super(LessThanZeroOp, self).__init__(
      name='LessThanZero',
      image='lessthanzero:v1',
      arguments = [
            '--data', data,
      ],
      file_outputs={
            'addLess': 'addData',
      })

class SumNumberOp(dsl.ContainerOp):
  """handle the number less than zero"""
  def __init__(self,data):
    super(SumNumberOp, self).__init__(
      name='SumNumberOp',
      image='sumnumber:v1',
      arguments = [
         '--data1', data1,
         '--data2', data2,
         '--data3', data3,
      ],
      file_outputs={
            'sumNumber': 'sumNumber',
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
    validate = validateOp(listData.outputs['listData'], splitNum)
    moreThanZero = MoreThanZeroOp(validate.outputs['more'])
    lessThanZero = LessThanZeroOp(validate.outputs['less'])
    sumNumber = SumNumberOp(lessThanZero.outputs['addLess'],moreThanZero.outputs['addMore'], listData)


compiler.Compiler().compile(ValData, 'test.yaml')