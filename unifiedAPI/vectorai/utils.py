import json
import torch
import base64


class Utils:

	@staticmethod
	def json_serializer(data):
		return json.dumps(data).encode("utf-8")

	@staticmethod
	def get_img_str(file):
		with open(file, "rb") as img_file:
			return base64.b64encode(img_file.read()).decode("utf-8")

	@staticmethod
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