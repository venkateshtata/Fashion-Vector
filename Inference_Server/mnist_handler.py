from torchvision import transforms
from ts.torch_handler.image_classifier import ImageClassifier
import torch


class MNISTDigitClassifier(ImageClassifier):

    image_processing = transforms.Compose([
        transforms.ToTensor()
    ])

    def postprocess(self, data):

        return data.argmax(1).tolist()
        
