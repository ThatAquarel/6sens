import numpy as np

from sixsens.audio import status
from sixsens.audio import nouns
from sixsens.reaction.reaction_builder import ReactionBuilder


class AudioReaction(ReactionBuilder):
    def __init__(self):
        self.sizes = {}
        self.distances = {}
        self.centroids = {}

    def _get_dist_string(self, distance_arr, frame_diag):
        obj_diag = np.min(distance_arr)
        percentage = obj_diag / frame_diag

        if percentage >= 0.25:
            dist_string = "CLOSE"
        elif percentage >= 0.125:
            dist_string = "10M"
        elif percentage >= 0.0625:
            dist_string = "20M"
        elif percentage >= 0.05:
            dist_string = "30M"
        elif percentage >= 0.04:
            dist_string = "40M"
        elif percentage >= 0.03:
            dist_string = "50M"
        else:
            dist_string = "PERIPHERY"

        return dist_string

    def process_predictions(self, latest):
        self.sizes.clear()
        self.distances.clear()
        self.centroids.clear()

        pred = latest.pred[0]

        for *box, conf, cls in reversed(pred):
            cls = int(cls)
            if not (key := latest.names[cls]) in self.sizes:
                self.sizes[key] = []
            self.sizes[key].append(
                np.sqrt((box[0] - box[2]) ** 2 + (box[1] - box[3]) ** 2)
            )

            if not key in self.centroids:
                self.centroids[key] = []
            self.centroids[key].append(
                [
                    (max(box[0], box[2]) - min(box[0], box[2])) / 2,
                    (max(box[1], box[3]) - min(box[1], box[3])) / 2,
                ]
            )

        frame_size = latest.ims[0].shape
        frame_diag = np.sqrt(frame_size[0] ** 2 + frame_size[1] ** 2)
        for key, value in self.sizes.items():
            self.distances[key] = self._get_dist_string(value, frame_diag)

    def build_reaction(self):
        speech = []
        noun = False

        def speech_condition(object_string, count):
            return (
                not len(speech)
                and object_string in self.sizes
                and len(self.sizes[object_string]) >= count
            )

        if speech_condition("traffic light", 1):
            speech.append(status.Attention())
            speech.append(nouns.Intersection())
            speech.append(nouns.Lights(self.distances["traffic light"]))

        if speech_condition("stop sign", 1):
            speech.append(nouns.Stop(self.distances["stop sign"]))

        if speech_condition("car", 1):
            speech.append(nouns.Car(self.distances["car"], "NONE"))

        if speech_condition("bus", 1):
            speech.append(nouns.Car(self.distances["bus"], "NONE"))

        if speech_condition("person", 1):
            ppl_count = len(self.sizes["person"])
            rounded_ppl_count = np.round(ppl_count / 10)
            if ppl_count == 1:
                ppl_class = nouns.People0
            elif rounded_ppl_count == 1:
                ppl_class = nouns.People10
            elif rounded_ppl_count == 2:
                ppl_class = nouns.People20
            elif rounded_ppl_count == 3:
                ppl_class = nouns.People30
            elif rounded_ppl_count == 4:
                ppl_class = nouns.People40
            elif rounded_ppl_count == 5:
                ppl_class = nouns.People50
            elif rounded_ppl_count >= 6:
                ppl_class = nouns.People100
            else:
                ppl_class = nouns.People1
            speech.append(ppl_class(self.distances["person"]))

        if speech_condition("chair", 1):
            speech.append(nouns.Chair(self.distances["chair"]))

        if speech_condition("table", 1):
            speech.append(nouns.Table(self.distances["table"]))

        return speech
