from vectorai import Kafka, Cloud

# kafka_config = {
# 	'bootstrap_servers': ['localhost:9092'],
# 	'topic': 'send_image',
# 	'model_server': 'http://127.0.0.1:8080/predictions/fashion',
# 	'group_id': 'consumer-group-a',
# 	'predictions_topic': 'get_predictions',
# 	'pred_group_id': 'pred_group'
# }

google_config = {
	'google_project_id': 'vectorai-329503',
	'google_topic_id': 'fashion',
	'google_subscription_id': 'get_fashion',
	'timeout': None,
	'model_server': 'http://127.0.0.1:8080/predictions/fashion',
	'google_predictions_topic_id': 'get_fashion_predictions'
}


client = Cloud(google_config) # set it to "ps" for using Google Pub/Sub and "kafka" to use Apache Kafka and change the config according to the service you want to use

client.consume_data()
