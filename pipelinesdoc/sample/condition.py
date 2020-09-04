import kfp
from kfp import dsl
from kubernetes import config
config.kube_config.load_kube_config(config_file="/etc/rancher/k3s/k3s.yaml")


def random_num_op(low, high):
    """Generate a random number between low and high."""
    return dsl.ContainerOp(
        name='Generate random number',
        image='python:alpine3.6',
        command=['sh', '-c'],
        arguments=['python -c "import random; print(random.randint($0, $1))" | tee $2', str(low), str(high), '/tmp/output'],
        file_outputs={'output': '/tmp/output'}
    )

@dsl.component
def flip_coin_op(inputData):
    """Flip a coin and output heads or tails randomly."""
    return dsl.ContainerOp(
        name='Flip coin',
        image='python:alpine3.6',
        command=['sh', '-c'],
        arguments=['python -c "import random; result = \'heads\' if $0 == 0 '
                  'else \'tails\'; print(result)" | tee $1', inputData , '/tmp/output'],
        file_outputs={'output': '/tmp/output'},
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
        flip = flip_coin_op()
        print_op('output_data  %s !' % flip.output)


        with dsl.Condition(flip.output == 'tails'):
            random_num_tail = random_num_op(10, 19)
            with dsl.Condition(random_num_tail.output > 15):
                print_op('tails and %s > 15!' % random_num_tail.output)
            with dsl.Condition(random_num_tail.output <= 15):
                print_op('tails and %s <= 15!' % random_num_tail.output)
        with dsl.Condition(flip.output == 'heads'):
            random_num_head = random_num_op(0, 9)
            with dsl.Condition(random_num_head.output > 5):
                print_op('heads and %s > 5!' % random_num_head.output)
            with dsl.Condition(random_num_head.output <= 5):
                print_op('heads and %s <= 5!' % random_num_head.output)



if __name__ == '__main__':
    kfp.compiler.Compiler().compile(flipcoin_pipeline, __file__ + '.yaml')