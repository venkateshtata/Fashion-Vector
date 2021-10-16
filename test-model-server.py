# Command : python3 test-model-server.py path/to/mnist-fashion-test-image

import requests
import base64
import sys
import torch


# map vector to prediction label
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

# inference server address
url = "http://127.0.0.1:8080/predictions/fashion"

# convert image to base64
with open(sys.argv[1], "rb") as img_file:
    my_string = base64.b64encode(img_file.read()).decode("utf-8") 

#add request headers
headers = {
  'Content-Type': 'text/plain'
}

# Make the request
response = requests.request("GET", url, headers=headers, data=my_string)

# Output prediction
print(output_label(int(response.text)))
