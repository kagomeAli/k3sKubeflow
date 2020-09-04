import kfp
from kfp import dsl

def flip_coin_op(train_data):
    """Flip a coin and output heads or tails randomly."""
    return dsl.ContainerOp(
        name= 'flip_coin',
        image='python:alpine3.6',
        command=['sh', '-c'],
        arguments=['echo $0 '
                  'else \'tails\'; print(result)" | tee $1', train_data , '/tmp/output'],
        file_outputs={'output': '/tmp/output'}
    )

def print_op(msg):
    """Print a message."""
    return dsl.ContainerOp(
        name='Print',
        image='alpine:3.6',
        command=['echo', msg],
    )


@dsl.pipeline(
    name='Conditional execution pipeline',
    description='Shows how to use dsl.function().'
)

def flipcoin_pipeline():
    train=dsl.PipelineParam(name='train', value='1')
    flip = flip_coin_op(train)
    print_op('output_data  %s !' % flip.output)



if __name__ == '__main__':
    kfp.compiler.Compiler().compile(flipcoin_pipeline, __file__ + '.yaml')