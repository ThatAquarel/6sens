import numpy as np

from sixsens.audio import status
from sixsens.audio import nouns


class AppReactionBuilder:
    def __init__(self):
        self.sizes = {}
        self.distances = {}
        self.centroids = {}

    def _get_dist_string(self, distance_arr):
        diag = np.min(distance_arr)
        dist = -2 * diag / 125 + 9
        dist = np.round(dist / 10)

        if dist == 0:
            dist_string = "CLOSE"
        elif dist == 1:
            dist_string = "10M"
        elif dist == 2:
            dist_string = "20M"
        elif dist == 3:
            dist_string = "30M"
        elif dist == 4:
            dist_string = "40M"
        elif dist == 5:
            dist_string = "50M"
        elif dist >= 6:
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
                [box[0] - box[2] / 2, box[1] - box[3] / 2]
            )

        for key, value in self.sizes.items():
            self.distances[key] = self._get_dist_string(value)

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
            speech.append(nouns.Car(self.distances["car"]))

        if speech_condition("bus", 1):
            speech.append(nouns.Car(self.distances["bus"]))

        if speech_condition("person", 2):
            ppl_count = np.round(len(self.sizes["person"]) / 10)
            if ppl_count == 1:
                ppl_class = nouns.People10
            elif ppl_count == 2:
                ppl_class = nouns.People20
            elif ppl_count == 3:
                ppl_class = nouns.People30
            elif ppl_count == 4:
                ppl_class = nouns.People40
            elif ppl_count == 5:
                ppl_class = nouns.People50
            elif ppl_count >= 6:
                ppl_class = nouns.People100
            else:
                ppl_class = nouns.People0
            speech.append(ppl_class(self.distances["person"]))

        if speech_condition("chair", 1):
            speech.append(nouns.Car(self.distances["chair"]))

        if speech_condition("table", 1):
            speech.append(nouns.Car(self.distances["table"]))

        return speech
