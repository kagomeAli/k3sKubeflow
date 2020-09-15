import json
import kfp
import kfp.containers as containers


thread = api.delete_experiment(id, async_req=True)
result = thread.get()