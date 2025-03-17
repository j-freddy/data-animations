import numpy as np
import pandas as pd


class Feature:
    def __init__(self, id: str, values: pd.Series, num_visible: int = 10):
        self.id = id
        self.values = values
        self.ranks = np.ones_like(values) * (num_visible + 1)

    def set_rank(self, rank, i):
        self.ranks[i] = rank
