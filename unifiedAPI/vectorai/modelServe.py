from .utils import Utils
import requests

class ModelServe:
	def __init__(self, url):
		self.url = url

	def get_prediction(self, img_data):
		headers = {
			'Content-Type': 'text/plain'
			}
		response = requests.request("GET", self.url, headers=headers, data=img_data)
		prediction = Utils.output_label(int(response.text))
		return(prediction)