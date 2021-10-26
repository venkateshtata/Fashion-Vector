import sys
import json
import time
from .utils import Utils
from .cloudCluster import CloudCluster
from .kafkaCluster import KafkaCluster
from abc import ABC, abstractmethod


class Consume(ABC):
	@abstractmethod
	def consume_data(self):
		pass


class Produce(ABC):
	@abstractmethod
	def produce_data(self):
		pass



class KafkaConnect(Consume, Produce):
	def __init__(self, config):
		self.config = config

	def produce_data(self, img_data):
		cluster = KafkaCluster(self.config)
		cluster.produce(img_data)

	def consume_data(self):
		cluster = KafkaCluster(self.config)
		cluster.consume()


class CloudConnect(Consume, Produce):
	def __init__(self, config):
		self.config = config

	def produce_data(self, img_data):
		cluster = CloudCluster(self.config)
		cluster.produce(img_data)

	def consume_data(self):
		cluster = CloudCluster(self.config)
		cluster.consume()
