from vectorai import Client

kafka_config = {
	'bootstrap_servers': ['localhost:9092'],
	'topic': 'send_image',
	'group_id': 'consumer-group-a'
}

google_config = {
	'google_project_id': 'vectorai-329503',
	'google_topic_id': 'fashion'
}

image_path = "/home/venkatesh/Desktop/vector_assignment/inference_test_images/test_image2.jpeg"


trail = Client("kafka", kafka_config) # set it to "ps" for using Google Pub/Sub and "kafka" to use Apache Kafka mand change the config according to the service you want to use

trail.produce(image_path)