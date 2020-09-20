import cv2
import json
import requests

headers = {"content-type": "application/json"}

json_response = requests.get("http://127.0.0.1:8882/")
predictions = json.loads(json_response.text)['predictions']

##curl -d '{"instances": [1.0,2.0,5.0]}' -X POST http://10.43.2.212:30002/v1/models/mnist:predict

print(predictions)