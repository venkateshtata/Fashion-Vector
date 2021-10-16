from kafka import KafkaProducer
import json
import time

import base64
import sys
import torch


def json_serializer(data):
	return json.dumps(data).encode("utf-8")

# def get_partition(key, all, available):
# 	reutrn 0



with open(sys.argv[1], "rb") as img_file:
	my_string = base64.b64encode(img_file.read()).decode("utf-8") 


producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=json_serializer)

if __name__ == "__main__":

	img = {"image": my_string}

	print("message :  ", img)
	producer.send("send_image", img)

	print("published!")

	producer.flush()