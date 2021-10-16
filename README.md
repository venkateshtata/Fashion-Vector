# Vector fashion

## Current Architecture

![Pipeline 0.1](https://github.com/venkateshtata/Fashion-Vector/blob/main/model_arch.png)

### Description

This repository implements pipeline for deploying a CNN trained on Fashion-MNIST dataset, into a distributed event streaming pipeline configured using Apache Kafta.



### Pre-requisites

The two main requisites for running this pipeline in your local system are Apache-Kafka and TorchServe :

* Head over to https://kafka.apache.org/quickstart and make sure ZooKeeper service and Kafka broker service, both are running.
* Install kafka-python with `pip3 install kafka-python`
* Install the requirements for [TorchServe](https://github.com/pytorch/serve)
* For better monitoring Kafka Cluster, install CMAK from https://github.com/yahoo/CMAK

### Testing Model Server

* The trained model is 93% accurate in classifying 10 different classes of Fasion-MNIST dataset, and the trained weights can be found in the root of this repo, where `weights.pt` is trained model inference with both model-architecture and weights included in it, whereas `best.pth` contains just the trained weights.
* Testing the model using the weight file :
  * `python3 test_model.py 4 (where x is an index of image within the test dataset, change for testing with different image)`
*  Testing the Model Server with Inference Endpoint :
  * First you need `cd` into Inference_Server directory, and run the below command to start the Model-Server.
  * `torchserve --start --model-store model_store --models fashion=model_store/fashion.mar`

### Interacting with the Model through Kafka Cluster

Note : Please make sure both the ZooKeeper and Kafka Broker services are both running before proceeding with below commands.

* Start subscribing by running `consumer.py` script in the kafka-app directory. It subcribes to the topic which recieves images from producer apps and publishes the predictions on `get_predictions` topic :
  * `python3 consumer.py` 
* The `producer.py` file (the producer app) in the same directory uses kafka-python to publish a payload with the image(as byte-string) passed as command-line argument to the `send_image` topic within the cluster :
  * `python3 producer.py path/to/image`
* Any app that is subscribed to the `get_predictions` topic would be recieving the inference predictions. To test it, run the following script : 
  * `python3 get_predictions` 

#### Topics Overview
- **/send_image** - Topic for publishing images.
- **/get_predictions** - Topic for getting predictions.
