import numpy as np

class Feature:
    def __init__(self, id, values, num_visible=10):
        self.id = id
        self.values = values
        self.ranks = np.ones_like(values) * (num_visible + 1)

    def set_rank(self, rank, i):
        self.ranks[i] = rank
