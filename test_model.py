import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
from torch.autograd import Variable

from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import confusion_matrix

import gzip
import struct


# Initializing the model architecture for testing
class FashionCNN(nn.Module):
	
	def __init__(self):
		super(FashionCNN, self).__init__()
		
		self.layer1 = nn.Sequential(
			nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1),
			nn.BatchNorm2d(32),
			nn.ReLU(),
			nn.MaxPool2d(kernel_size=2, stride=2)
		)
		
		self.layer2 = nn.Sequential(
			nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3),
			nn.BatchNorm2d(64),
			nn.ReLU(),
			nn.MaxPool2d(2)
		)
		
		self.fc1 = nn.Linear(in_features=64*6*6, out_features=600)
		self.drop = nn.Dropout2d(0.25)
		self.fc2 = nn.Linear(in_features=600, out_features=120)
		self.fc3 = nn.Linear(in_features=120, out_features=10)
		
	def forward(self, x):
		out = self.layer1(x)
		out = self.layer2(out)
		out = out.view(out.size(0), -1)
		out = self.fc1(out)
		out = self.drop(out)
		out = self.fc2(out)
		out = self.fc3(out)
		
		return out

model = FashionCNN()

#loading the pre-trained weights
model = torch.load("weights.pt")
model.eval()

# mfunction to return the name of class for the label number
def output_label(label):
	output_mapping = {
				 0: "T-shirt/Top",
				 1: "Trouser",
				 2: "Pullover",
				 3: "Dress",
				 4: "Coat", 
				 5: "Sandal", 
				 6: "Shirt",
				 7: "Sneaker",
				 8: "Bag",
				 9: "Ankle Boot"
				 }

	input = (label.item() if type(label) == torch.Tensor else label)
	return output_mapping[input]

# Test set location
test_set = '/home/venkatesh/Desktop/vector_assignment/tet_set/t10k-images-idx3-ubyte.gz'
test_images = []


# Creating test set array 
with gzip.open(test_set,'rb') as f:
	magic, size = struct.unpack(">II", f.read(8))
	nrows, ncols = struct.unpack(">II", f.read(8))
	data = np.frombuffer(f.read(), dtype=np.dtype(np.uint8).newbyteorder('>'))
	data = data.reshape((size, nrows, ncols))

	test_images.append(data)
test_images = np.array(test_images)


# Getting the test image
test_image_no = int(sys.argv[1])

# Converting to torch tensor
image = torch.tensor(test_images[0][test_image_no])


#changing view of input vector dimention
image = Variable(image.view(1, 1, 28, 28))


# Displaying selected test mage
plt.imshow(test_images[0][test_image_no,:,:], cmap='gray')	
plt.show()

# Getting predictions
pred = model(image.float())

#Output predicted fashion!
print("Prediction : ",output_label(torch.argmax(pred)))
