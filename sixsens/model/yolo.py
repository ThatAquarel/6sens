import torch

from sixsens.model.pipeline import PipelineNode


class YoloNode(PipelineNode):
    def setup(self):
        self.model = torch.hub.load("ultralytics/yolov5", "yolov5n")

    def process(self, frame):
        results = self.model(frame)
        return (results, results.render()[0])

    def render(self, frame):
        pass
