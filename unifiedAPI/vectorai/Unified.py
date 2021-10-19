from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
import time
import base64
import sys
import requests
import torch
from google.cloud import pubsub_v1

# For using the Google Pub/Sub you need to export GOOGLE_APPLICATION_CREDENTIALS= path/to/api-key.json file.

class Unified():

	def __init__(self, broker_type):
		self.broker_type = broker_type


	def json_serializer(self, data):
		return json.dumps(data).encode("utf-8")


	def get_img_str(self, file):
		with open(file, "rb") as img_file:
			return base64.b64encode(img_file.read()).decode("utf-8")


	def output_label(self, label):
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


	def pub(self, project_id: str, topic_id: str, img: str) -> None:
		"""Publishes a message to a Pub/Sub topic."""

		# Initialize a Publisher client.
		client = pubsub_v1.PublisherClient()

		# Create a fully qualified identifier of form `projects/{project_id}/topics/{topic_id}`
		topic_path = client.topic_path(project_id, topic_id)

		# Data sent to Cloud Pub/Sub must be a bytestring.
		data = bytes(img, 'utf-8')

		# When you publish a message, the client returns a future.
		api_future = client.publish(topic_path, data)
		message_id = api_future.result()

		print(f"Published to Pub/Sub Topic: {topic_path}, with message ID: {message_id}")


	def sub(self, project_id: str, url: str, subscription_id: str, timeout: float = None) -> None:
		"""Receives messages from a Pub/Sub subscription."""

		# Initialize a Subscriber client
		subscriber_client = pubsub_v1.SubscriberClient()

		# Create a fully qualified identifier in the form of
		# `projects/{project_id}/subscriptions/{subscription_id}`
		subscription_path = subscriber_client.subscription_path(project_id, subscription_id)

		def callback(message: pubsub_v1.subscriber.message.Message) -> None:
			print(f"Received {message}.")

			headers = {
				'Content-Type': 'text/plain'
				}

			response = requests.request("GET", url, headers=headers, data=message.data)
			prediction = self.output_label(int(response.text))
			print("prediction : ", prediction)




			# Acknowledge the message. Unack'ed messages will be redelivered.
			message.ack()
			print(f"Acknowledged {message.message_id}.")

		streaming_pull_future = subscriber_client.subscribe(
			subscription_path, callback=callback
		)
		print(f"Listening for messages on {subscription_path}..\n")

		try:

			# Calling result() on StreamingPullFuture keeps the main thread from
			# exiting while messages get processed in the callbacks.
			streaming_pull_future.result(timeout=timeout)
		except:  # noqa

			streaming_pull_future.cancel()  # Trigger the shutdown.
			streaming_pull_future.result()  # Block until the shutdown is complete.

		subscriber_client.close()



	def produce(self, config, img_path) -> None:
		if(self.broker_type == "kafka"):
			producer = KafkaProducer(bootstrap_servers=config['bootstrap_servers'], value_serializer=self.json_serializer)
			img_str = self.get_img_str(img_path)
			img_payload = {"image": img_str}
			producer.send(config['topic'], img_payload)
			producer.flush()
			print("Published data to {}".format(config['topic']))

		if(self.broker_type == "ps"):
			img_str = self.get_img_str(img_path)
			self.pub(config['google_project_id'], config['google_topic_id'], img_str)


	def consume(self, config) -> None:
		if(self.broker_type == "kafka"):
			print("Listening to topic : {}".format(config['topic']))

			consumer = KafkaConsumer(config['topic'], bootstrap_servers=config['bootstrap_servers'], auto_offset_reset="earliest", group_id=config['group_id'])
			
			headers = {
				'Content-Type': 'text/plain'
				}

			for msg in consumer:
				img_data = json.loads(msg.value)['image']
				url = config['model_server']

				# Make the request
				response = requests.request("GET", url, headers=headers, data=img_data)
				prediction = self.output_label(int(response.text))
				print(prediction)

				producer = KafkaProducer(bootstrap_servers=config['bootstrap_servers'], value_serializer=self.json_serializer)
				producer.send(config['predictions_topic'], prediction)
				producer.flush()

		if(self.broker_type == "ps"):
			self.sub(config['google_project_id'], config['model_server'], config['google_subscription_id'], config['timeout'])



	def get_predictions(self, config) -> None:
		print("Listening for predictions at topic : {}".format(config['predictions_topic']))
		consumer = KafkaConsumer(config['predictions_topic'], bootstrap_servers=config['bootstrap_servers'], auto_offset_reset="earliest", group_id=config['pred_group_id'])

		for msg in consumer:
			prediction = json.loads(msg.value)
			print("prediction : ", prediction)

		
