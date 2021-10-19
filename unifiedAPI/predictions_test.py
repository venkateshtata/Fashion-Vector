from vectorai import Unified

trail = Unified("kafka")

config = {
	'bootstrap_servers': ['localhost:9092'],
	'topic': 'send_image',
	'model_server': 'http://127.0.0.1:8080/predictions/fashion',
	'group_id': 'consumer-group-a',
	'predictions_topic': 'get_predictions',
	'pred_group_id': 'pred_group'
}


trail.get_predictions(config) 