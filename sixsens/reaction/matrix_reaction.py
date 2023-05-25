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
        self.scalar = np.ones(2, np.float)
        self.matrix = np.zeros((self.ROWS, self.COLS), np.uint8)

    def process_predictions(self, latest):
        self.scalar = np.divide((self.ROWS, self.COLS), (latest.ims[0].shape))

        self.centroids.clear()
        pred = latest.pred[0]

        for *box, conf, cls in reversed(pred):
            cls = int(cls)
            if not (key := latest.names[cls]) in self.centroids:
                self.centroids[key] = []
            self.centroids[key].append(
                [box[0] - box[2] / 2, box[1] - box[3] / 2]
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

        self.matrix[centroids[:, 0], centroids[:, 1]] = 255
        self.matrix[-1, -1] = 0
        return centroids.flatten()
