from abc import ABC, abstractmethod


class PipelineNode(ABC):
    def __init__(self):
        super().__init__()
        self.setup()

    @abstractmethod
    def setup(self):
        raise NotImplementedError()

    @abstractmethod
    def process(self, frame):
        raise NotImplementedError()
