import json
import kfp
import kfp.dsl as dsl


_CONTAINER_MANIFEST = """
{
    "apiVersion": "batch/v1",
    "kind": "Job",
    "metadata": {
        "generateName": "resourceop-basic-job-"
    },
    "spec": {

"""


@dsl.pipeline(
    name="ResourceOp Basic",
    description="A Example on ResourceOp Usage."
)
def resourceop_basic():
    # Start a container. Print out env vars.
    op = dsl.ResourceOp(
        name='test-step',
        k8s_resource=json.loads(_CONTAINER_MANIFEST),
        action='create'
    )


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(resourceop_basic, __file__ + '.yaml')