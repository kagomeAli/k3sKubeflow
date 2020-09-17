import kfp
import kfp.compiler as compiler
client = kfp.Client()

id='5b964de5-60ad-406a-b6d9-dfe7e7c3012c'
run = client.list_runs(experiment_id=id,job_name='fabric_name')
#creat_exper = client.create_experiment(name='test_fabric')
# 5a00f267-cbb8-4f4d-a1f4-fc1e5bcde23e
#list_exper = cient.delete_pipeline(pipeline_id='900d9827-c8b4-4c52-b72e-91f5ddfcc588')

# my_experiment = client.create_experiment(name='demo')
my_run = client.run_pipeline('5a00f267-cbb8-4f4d-a1f4-fc1e5bcde23e', 'fabricModel')

