from dataclasses import dataclass
import pandas as pd
import numpy as np


@dataclass
class DataSeries:
    """
    Represent a time series of data values for a single entity with support for
    storing the associated rankings over time.

    This class is not responsible for any calculations. For example, the
    rankings are set to num_visible + 1 by default.

    Attributes:
        id (str): Unique identifier for this data series.
        values (pd.Series): Time series of measurements or observations.
        ranks (np.ndarray): Array containing the rank of this series at each
            timestamp.
    """

    id: str
    values: pd.Series
    num_visible: int = 10

    def __post_init__(self) -> None:
        self.ranks = np.ones_like(self.values) * (self.num_visible + 1)

    def set_rank(self, rank: int, i: int) -> None:
        self.ranks[i] = rank
