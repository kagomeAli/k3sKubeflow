import kfp
from kfp import dsl

@dsl.pipeline(
    name='Conditional execution pipeline',
    description='Shows how to use dsl.Condition().'
)
def flipcoin_pipeline():
    dslArgs = dsl.PipelineParam(name='tfma-mode', value='local')
    print(dslArgs.name)
    print(dslArgs.value)


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(flipcoin_pipeline, __file__ + '.yaml')