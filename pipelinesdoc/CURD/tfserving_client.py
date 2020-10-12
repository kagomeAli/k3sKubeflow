import cv2
import json
import requests

img = cv2.imread('0_100.jpg', cv2.IMREAD_GRAYSCALE)

img = img / 255.0

img = img.reshape(-1, 128, 128, 1).tolist()

data = json.dumps({"signature_name": "serving_default", "instances": img})

headers = {"content-type": "application/json"}
json_response = requests.post("http://10.43.105.52:8500/v1/models/back:predict", data=data, headers=headers)
predictions = json.loads(json_response.text)['predictions']
print(predictions)