from abc import ABC, abstractmethod

class ClusterOperations(ABC):

    @abstractmethod
    def produce(self, img_path):
        pass

    @abstractmethod
    def consume(self):
        pass