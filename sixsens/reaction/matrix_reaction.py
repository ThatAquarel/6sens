import numpy as np

from sixsens.reaction.reaction_builder import ReactionBuilder


class MatrixReaction(ReactionBuilder):
    PRIORITY = [
        "traffic light",
        "stop sign",
        "car",
        "bus",
        "person",
        "chair",
        "table",
    ]

    ROWS = 8
    COLS = 6

    def __init__(self):
        self.centroids = {}
        self.scalar = np.zeros(2, dtype=np.float)
        self.matrix = np.zeros((self.COLS, self.ROWS), dtype=np.uint8)

    def process_predictions(self, latest):
        self.scalar[:] = [self.COLS, self.ROWS]
        self.scalar /= latest.ims[0].shape[0:2]

        self.centroids.clear()
        pred = latest.pred[0]

        for *box, conf, cls in reversed(pred):
            cls = int(cls)
            if not (key := latest.names[cls]) in self.centroids:
                self.centroids[key] = []
            self.centroids[key].append(
                [
                    (max(box[0], box[2]) - min(box[0], box[2])) / 2,
                    (max(box[1], box[3]) - min(box[1], box[3])) / 2,
                ]
            )

    def build_reaction(self):
        selected_centroids = None
        for key in self.PRIORITY:
            if not key in self.centroids:
                continue
            if len((centroids := self.centroids[key])) < 1:
                continue

            selected_centroids = centroids
            break

        self.matrix[:] = 0
        if not selected_centroids:
            return self.matrix
        centroids = selected_centroids

        centroids = np.multiply(centroids, self.scalar)
        centroids = np.floor(centroids)
        centroids = np.clip(centroids, [0, 0], [self.ROWS - 1, self.COLS - 1])
        centroids = centroids.astype(int)

        self.matrix[centroids[:, 0], centroids[:, 1]] = 255
        self.matrix[-1, -1] = 0

        return self.matrix.flatten()
