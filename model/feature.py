import numpy as np

from model.const import NUM_VISIBLE

class Feature:
    def __init__(self, id, values):
        self.id = id
        self.values = values
        self.ranks = np.ones_like(values) * (NUM_VISIBLE + 1)

    def set_rank(self, rank, i):
        self.ranks[i] = rank
