from vectorai import Unified

kafka_config = {
	'bootstrap_servers': ['localhost:9092'],
	'topic': 'send_image',
	'model_server': 'http://127.0.0.1:8080/predictions/fashion',
	'group_id': 'consumer-group-a',
	'predictions_topic': 'get_predictions',
	'pred_group_id': 'pred_group'
}

google_config = {
	'google_project_id': 'vectorai-329503',
	'google_topic_id': 'fashion'
}

image_path = "/home/venkatesh/Desktop/vector_assignment/inference_test_images/test_image2.jpeg"


trail = Unified("ps") # set it to "ps" for using Google Pub/Sub and "kafka" to use Apache Kafka
trail.produce(google_config, image_path) # change the config according to the service you want to use
