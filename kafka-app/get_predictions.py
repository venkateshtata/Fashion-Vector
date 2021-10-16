from kafka import KafkaConsumer
from kafka import KafkaProducer
import json
import requests
import base64
import sys
import torch





consumer = KafkaConsumer("get_predictions", bootstrap_servers="localhost:9092", auto_offset_reset="earliest", group_id="consumer-group-b")

print("Listening for predictions")

for msg in consumer:

	preds = json.loads(msg.value)
	print("prediction : ", preds)