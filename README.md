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

* 
