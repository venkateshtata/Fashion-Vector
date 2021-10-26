from .utils import Utils
from .modelServe import ModelServe
from .clusterInterface import ClusterOperations
from google.cloud import pubsub_v1

class CloudCluster(ClusterOperations):

	def __init__(self, config):
		self.config = config

	def pub(self, project_id: str, topic_id: str, img: str) -> None:
		client = pubsub_v1.PublisherClient()
		topic_path = client.topic_path(project_id, topic_id)
		data = bytes(img, 'utf-8')
		api_future = client.publish(topic_path, data)
		message_id = api_future.result()
		print(f"Published to Pub/Sub Topic: {topic_path}, with message ID: {message_id}")


	def sub(self, project_id: str, url: str, subscription_id: str, timeout: float = None) -> None:
		subscriber_client = pubsub_v1.SubscriberClient()
		subscription_path = subscriber_client.subscription_path(project_id, subscription_id)

		def callback(message: pubsub_v1.subscriber.message.Message) -> None:
			print(f"Received {message}.")

			model = ModelServe(url)
			prediction = model.get_prediction(message.data)

			print("Prediction : ", prediction)

			message.ack()
			print(f"Acknowledged {message.message_id}.")
		streaming_pull_future = subscriber_client.subscribe(
			subscription_path, callback=callback
		)
		print(f"Listening for messages on {subscription_path}..\n")
		try:
			streaming_pull_future.result(timeout=timeout)
		except:  # noqa
			streaming_pull_future.cancel()  # Trigger the shutdown.
			streaming_pull_future.result()  # Block until the shutdown is complete.
		subscriber_client.close()

	def produce(self, img_path):
		img_str = Utils.get_img_str(img_path)
		self.pub(self.config['google_project_id'], self.config['google_topic_id'], img_str)
	

	def consume(self):
		self.sub(self.config['google_project_id'], self.config['model_server'], self.config['google_subscription_id'], self.config['timeout'])