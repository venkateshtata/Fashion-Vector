# Vector Fashion

Vectorai is a library that can be used to communicate with Apache Kafka Cluster or the Google Cloud Pub/Sub to publish images and subscribe to predictions.


### Pre-requisites

The two main requisites for running this pipeline in your local system are Apache-Kafka and TorchServe :

* Head over to https://kafka.apache.org/quickstart and make sure ZooKeeper service and Kafka broker service, both are running.
* Install kafka-python with `pip3 install kafka-python`
* Install the requirements for [TorchServe](https://github.com/pytorch/serve)
* (Optional) For better monitoring Kafka Cluster, install CMAK from https://github.com/yahoo/CMAK
* export GOOGLE_APPLICATION_CREDENTIALS=path/to/api-key.json file in the working terminal or add it as an environemt variable for using vectorai with Cloud Pub/Sub.

### Testing Model Server

* The trained model is 93% accurate in classifying 10 different classes of Fashion-MNIST dataset, and the trained weights can be found in the root of this repo, where `weights.pt` is trained model inference with both model-architecture and weights included in it, whereas `best.pth` contains just the trained weights.
* Testing the model using the weight file :
  * `python3 test_model.py 4 (where 4 is an index of image within the test dataset, change for testing with different image)`
*  Testing the Model Server with Inference Endpoint :
  * First you need `cd` into Inference_Server directory, and run the below command to start the Model-Server.
  * `torchserve --start --model-store model_store --models fashion=model_store/fashion.mar`
  * Then run `python3 test-model-server.py path/to/mnist-fashion-test-image` for getting predictions over HTTP from TorchServe.

### Interacting with the Model through Kafka and Cloud Pub/Sub using vectorai : 

Note : Please make sure both the ZooKeeper and Kafka Broker services are both running before proceeding with below commands.

* In order for using the Unified class methods from vectorai module, the config object has to be created with required properties as required by Kafka or Cloud Pub/Sub, according which you want to communicate with.
*  Below is an example for listening to a topic on Kafka Cluster :

```
from vectorai import Unified

kafka_config = {
	'bootstrap_servers': ['localhost:9092'],
	'topic': 'send_image',
	'model_server': 'http://127.0.0.1:8080/predictions/fashion',
	'group_id': 'consumer-group-a',
	'predictions_topic': 'get_predictions',
	'pred_group_id': 'pred_group'
}

trail = Unified("kafka") # set it to "ps" for using Google Pub/Sub and "kafka" to use Apache Kafka
trail.consume(kafka_config) # change the config according to the service you want to use

```

* Example for publishing to a topic on Kafka Cluster  :
```
from vectorai import Unified

kafka_config = {
	'bootstrap_servers': ['localhost:9092'],
	'topic': 'send_image',
	'model_server': 'http://127.0.0.1:8080/predictions/fashion',
	'group_id': 'consumer-group-a',
	'predictions_topic': 'get_predictions',
	'pred_group_id': 'pred_group'
}

image_path = "path/to/image"

trail = Unified("kafka") # set it to "ps" for using Google Pub/Sub and "kafka" to use Apache Kafka
trail.produce(kafka_config, image_path) # change the config according to the service you want to use

```
* Example for subscribing to Cloud Pub/Sub using vectorai :
```
from vectorai import Unified

google_config = {
	'google_project_id': 'vectorai-329503',
	'google_topic_id': 'fashion',
	'google_subscription_id': 'get_fashion',
	'timeout': None,
	'model_server': 'http://127.0.0.1:8080/predictions/fashion',
	'google_predictions_topic_id': 'get_fashion_predictions'
}


trail = Unified("ps") # set it to "ps" for using Google Pub/Sub and "kafka" to use Apache Kafka
trail.consume(google_config) # change the config according to the service you want to use

```
* Example for publishing to Cloud Pub/Sub using vectorai :
```
from vectorai import Unified

google_config = {
	'google_project_id': 'vectorai-329503',
	'google_topic_id': 'fashion'
}

image_path = "path/to/image"


trail = Unified("ps") # set it to "ps" for using Google Pub/Sub and "kafka" to use Apache Kafka
trail.produce(google_config, image_path) # change the config according to the service you want to use

```
