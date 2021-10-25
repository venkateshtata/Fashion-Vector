from .utils import Utils
from .modelServe import ModelServe
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
from .clientInterface import ClusterOperations


class KafkaCluster(ClusterOperations):

	def __init__(self, config):
		self.config = config

	def produce(self, img_path):
		producer = KafkaProducer(bootstrap_servers=self.config['bootstrap_servers'], value_serializer=Utils.json_serializer)
		img_str = Utils.get_img_str(img_path)
		img_payload = {"image": img_str}
		producer.send(self.config['topic'], img_payload)

		#block until all async messages are sent
		producer.flush()
		print("Published data to {}".format(self.config['topic']))

	def consume(self):
		print("Listening to topic : {}".format(self.config['topic']))
		consumer = KafkaConsumer(self.config['topic'], bootstrap_servers=self.config['bootstrap_servers'], auto_offset_reset="earliest", group_id=self.config['group_id'])

		for msg in consumer:
			img_data = json.loads(msg.value)['image']
			url = self.config['model_server']

			model = ModelServe(url)
			prediction = model.get_prediction(img_data)

			print("Prediction : ", prediction)

			producer = KafkaProducer(bootstrap_servers=self.config['bootstrap_servers'], value_serializer=Utils.json_serializer)
			producer.send(self.config['predictions_topic'], prediction)

			#block until all async messages are sent
			producer.flush()