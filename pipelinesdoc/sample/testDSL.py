import kfp
from kfp import dsl

@dsl.pipeline(
    name='Conditional execution pipeline',
    description='Shows how to use dsl.Condition().'
)


def flipcoin_pipeline():
    createModel = dsl.ContainerOp(
        name="create_model",
        image="yanqin/request:v1",
        file_outputs={'output': '/data/file1'},
        pvolumes={"/data": dsl.PipelineVolume(pvc="hostpath-pvc")}
    )


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(flipcoin_pipeline, __file__ + '.yaml')