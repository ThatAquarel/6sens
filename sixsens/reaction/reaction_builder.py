from abc import ABC, abstractmethod


class ReactionBuilder:
    @abstractmethod
    def process_predictions(self):
        raise NotImplementedError()

    @abstractmethod
    def build_reaction(self):
        raise NotImplementedError()
