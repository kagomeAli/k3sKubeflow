import cv2
import json
import requests

img = cv2.imread('0_1.jpg', cv2.IMREAD_GRAYSCALE)
img = img / 255.0
img = img.reshape(-1, 128, 128, 1).tolist()
data = json.dumps({"signature_name": "serving_default", "instances": img})
headers = {"content-type": "application/json"}
json_response = requests.post("http://10.43.70.68:8501/v1/models/fabric:predict", data=data, headers=headers)
predictions = json.loads(json_response.text)['predictions']

##curl -d '{"instances": [1.0,2.0,5.0]}' -X POST http://140.115.53.52:30009/v1/models/mnist:predict

print(predictions)