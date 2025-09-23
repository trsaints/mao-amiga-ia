from abc import ABC, abstractmethod

class MachineLearningModel(ABC):
    @abstractmethod
    def load_data(self, file_path, target_column):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def save_model(self, file_path):
        pass
