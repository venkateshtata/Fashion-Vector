from kafka import KafkaConsumer
from kafka import KafkaProducer
import json
import requests
import base64
import sys
import torch


def output_label(label):
	output_mapping = {
				 0: "T-shirt/Top",
				 1: "Trouser",
				 2: "Pullover",
				 3: "Dress",
				 4: "Coat", 
				 5: "Sandal", 
				 6: "Shirt",
				 7: "Sneaker",
				 8: "Bag",
				 9: "Ankle Boot"
				 }

	input = (label.item() if type(label) == torch.Tensor else label)
	return output_mapping[input]


# inference server address
url = "http://127.0.0.1:8080/predictions/fashion"

#add request headers
headers = {
	'Content-Type': 'text/plain'
}

def json_serializer(data):
	return json.dumps(data).encode("utf-8")

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=json_serializer)
consumer = KafkaConsumer("send_image", bootstrap_servers="localhost:9092", auto_offset_reset="earliest", group_id="consumer-group-a")

print("Starting the consumer")

for msg in consumer:

	img_data = json.loads(msg.value)['image']

	# Make the request
	response = requests.request("GET", url, headers=headers, data=img_data)

	producer.send("get_predictions", output_label(int(response.text)))

	print("published to topic: /get_predictions ")

	producer.flush()

	print(output_label(int(response.text)))
