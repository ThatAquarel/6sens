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

    ROWS = 6
    COLS = 8

    CROP_0 = (860, 75)
    CROP_1 = (1845, 1005)

    def __init__(self):
        self.centroids = {}
        self.scalar = np.divide(
            [self.COLS, self.ROWS], np.subtract(self.CROP_1, self.CROP_0)
        )

        self.matrix = np.zeros((self.COLS, self.ROWS), dtype=np.uint8)

    def process_predictions(self, latest):
        self.centroids.clear()
        pred = latest.pred[0]

        for *box, conf, cls in reversed(pred):
            cls = int(cls)
            if not (key := latest.names[cls]) in self.centroids:
                self.centroids[key] = []
            self.centroids[key].append(
                [
                    (box[0] + box[2]) / 2,
                    (box[1] + box[3]) / 2,
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
            return self.matrix.flatten()

        centroids = np.array(selected_centroids)

        centroids[:, 0] -= self.CROP_0[0]
        centroids[:, 1] -= self.CROP_0[1]

        centroids = np.multiply(centroids, self.scalar)
        centroids = np.floor(centroids)
        centroids = np.clip(centroids, [0, 0], [self.COLS - 1, self.ROWS - 1])

        centroids = centroids.astype(int)

        self.matrix[centroids[:, 0], centroids[:, 1]] = 255
        self.matrix[:, -1] = 0
        self.matrix = self.matrix[::-1]

        return self.matrix.flatten()
