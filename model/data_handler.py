import os
import numpy as np
import pandas as pd

from model.const import BAR_WIDTH_LERP_KERNEL_SIZE, DIR_IN
from model.data_series import DataSeries
from model.lerp import Lerp


class DataHandler:
    """
    Handles loading, processing, and providing access to time series data for
    bar chart animations.

    This class loads CSV data, creates DataSeries objects for each series,
    calculates appropriate visualization parameters (like units, rankings, and
    maximum values) and provides methods to access these values for smooth
    animations.

    This DataHandler is not responsible for raw data processing and does not
    act as a replacement for the ETL pipeline. The CSV data must respect the
    following criteria.
    1. The first column must contain evenly spaced timestamps. Otherwise, the
       animation will speed up and slow down according to the spacing.
    2. The first row must contain series names.
    3. The remaining cells, apart from the timestamps, must be numerical.

    For an example, see data/example.csv.
    """

    def __init__(self, filename: str, num_visible: int = 10) -> None:
        """
        Initialize the DataHandler with data from a CSV file.

        Loads the specified CSV file, processes the data to create DataSeries
        objects, calculates visualization parameters like units and rankings,
        and prepares the data for bar chart animation rendering.

        The CSV data must respect the following criteria.
        1. The first column must contain evenly spaced timestamps. Otherwise,
           the animation will speed up and slow down according to the spacing.
        2. The first row must contain series names.
        3. The remaining cells, apart from the timestamps, must be numerical.

        Args:
            filename (str): Name of the CSV file (without extension) to load
                from DIR_IN.
            num_visible (int, optional): Maximum number of bars to display in
                the visualization. Default: 10.
        """
        self.data = pd.read_csv(os.path.join(DIR_IN, f"{filename}.csv"))
        # Drop rows where all elements are NaN (e.g. empty lines at end of file)
        self.data = self.data.dropna(how="all")

        self.num_visible = num_visible

        self.data_series = {
            name: DataSeries(name, series.values, num_visible)
            for name, series in self._get_series().items()
        }

        # Available units
        base = np.array([1, 2, 5])
        exp_limit = int(np.ceil(np.log10(self._get_max())))

        self.available_units = np.outer(
            np.power(10, np.arange(0, exp_limit)),
            base,
        ).ravel()

        # Perform calculations

        # Ids of series that are visible per timestamp
        self.top_series_ids = self._get_top_series_ids()

        # Max series value per timestamp
        self.maxes = self._get_maxes()

        # Unit choice per timestamp
        # Usage: self.available_units[self.units_indices[timestamp_index]]
        self.units_indices = self._get_units_indices()

        self.update_ranks()

    def _get_series(self) -> pd.DataFrame:
        """
        Get the raw data without the timestamp column.
        """
        return self.data.iloc[:, 1:]

    def _get_max(self) -> float:
        """
        Get the maximum value in the data.
        """
        return self._get_series().max().max()

    def _get_maxes(self) -> pd.Series:
        """
        Get the maximum value per series.
        """
        return self._get_series().max(axis=1)

    def _get_top_series_ids(self) -> pd.Series:
        return self._get_series().apply(
            lambda timestamp: timestamp.nlargest(self.num_visible).index.to_numpy(),
            axis=1,
        )

    def _get_units_indices(self) -> np.ndarray:
        """
        For the entire time series, compute the most appropriate set of bar plot
        ticks. The indices correspond to the list self.available_units.
        """
        units_indices = np.empty(self.num_series())

        for i in range(self.num_series()):
            max_bar_width = self.calculate_max_bar_width_value(i)

            # Choose appropriate unit
            min_ticks = 3
            # Choose largest unit that is not too large (i.e. shows at least
            # @min_ticks ticks)
            units_indices[i] = (
                np.where((self.available_units * min_ticks) > max_bar_width)[0][0] - 1
            )

        return units_indices

    def num_series(self) -> int:
        """
        Get the number of series in the data.
        """
        return self._get_series().shape[0]

    def get_timestamp(self, i):
        """
        Get the timestamp of the i-th entry.
        """
        return self.data.values[i, 0]

    def calculate_max_bar_width_value(self, timestamp_index: float) -> float:
        """
        At a given timestamp, the max bar width value is the corresponding value
        of a hypothetical bar that takes the entire screen width.

        For example, if the time series context is city population, and in year
        1990 the city with the largest population has 10 million people, then
        the max bar width value is around 11.5 million.

        This ensures that the largest bar never stretches the entire screen
        width and is more visually appealing.

        Args:
            timestamp_index (float): The index of the timestamp in the data.

        Returns:
            float: The max bar width value.
        """
        return (
            Lerp.weighted_avg(
                self.maxes, timestamp_index, kernel_size=BAR_WIDTH_LERP_KERNEL_SIZE
            )
            * 1.15
        )

    def update_ranks(self) -> None:
        """
        Update the rank of each series at every timestamp.

        The update is done lazily. At each timestamp, only the top visible
        series are updated.
        """
        for i, series_ids in enumerate(self.top_series_ids):
            for rank, series_id in enumerate(series_ids):
                self.data_series[series_id].set_rank(rank, i)
