import sys
import json
import time
from .utils import Utils
from .cloudCluster import CloudCluster
from .kafkaCluster import KafkaCluster


class Client():

	def __init__(self, broker_type, config):
		self.broker_type = broker_type
		self.config = config

	def consume(self):

		if(self.broker_type=="kafka"):
			cluster = KafkaCluster(self.config)
			cluster.consume()
		elif(self.broker_type=="ps"):
			cluster = CloudCluster(self.config)
			cluster.consume()

	def produce(self, img_path):

		if(self.broker_type=="kafka"):
			cluster = KafkaCluster(self.config)
			cluster.produce(img_path)
		elif(self.broker_type=="ps"):
			cluster = CloudCluster(self.config)
			cluster.produce(img_path)



