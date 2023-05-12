from sixsens.audio import status
from sixsens.audio import nouns


class AppReactionBuilder:
    def __init__():
        self.sizes = {}
        self.distances = {}

    def process_predictions(pred):
        for *box, conf, cls in reversed(pred):
            cls = int(cls)
            if not (key := latest.names[cls]) in self.sizes:
                self.sizes[key] = []
            self.sizes[key].append(
                np.sqrt((box[0] - box[2]) ** 2 + (box[1] - box[3]) ** 2)
            )
        for key, value in self.sizes.items():
            self.distances[key] = get_dist_string(value)

    def build_reaction():
        speech = []
        noun = False

        def speech_condition(object_string, count):
            return (
                not len(speech)
                and object_string in self.sizes
                and len(sizes[object_string]) >= count
            )

        if speech_condition("traffic light", 1):
            speech.append(status.Attention())
            speech.append(status.Intersection())
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
