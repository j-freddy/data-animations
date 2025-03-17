import numpy as np
import pandas as pd


class Lerp:
    """
    Provides static methods for linear interpolation and weighted averaging.

    This class contains utility methods for interpolating values from pandas
    Series, including simple linear interpolation and weighted averaging with a
    cosine kernel.
    """

    @staticmethod
    def linear(series: pd.Series, index: float) -> float:
        """
        Performs linear interpolation between adjacent elements at a given index
        in a pandas Series.

        Args:
            series (pd.Series): Source Series to interpolate from. index (float):
            Interpolated index of Series.

        Returns:
            float: Interpolated value.
        """

        before = series[int(index)]
        after = series[min(len(series) - 1, int(index) + 1)]
        return np.interp(index % 1.0, [0, 1], [before, after])

    @staticmethod
    def weighted_avg(series: pd.Series, index: float, kernel_size: int) -> float:
        """
        Calculates weighted average of Series elements at a given index in a
        pandas Series using a cosine kernel.

        Args:
            series (pd.Series): Source Series for weighted averaging.
            index (float): Center position for the kernel window.
            kernel_size (int): Size of the kernel window. Must be odd.
                Determines how many elements are included in the weighted
                average.

        Returns:
            float: Weighted average.

        Raises:
            ValueError: If kernel_size is not odd.
        """

        if kernel_size % 2 == 0:
            raise ValueError("Kernel size must be an odd number.")

        tail_size = kernel_size // 2

        low = int(max([0, np.ceil(index - tail_size)]))
        high = int(min([len(series) - 1, np.floor(index + tail_size)]))

        weights = 0.5 + 0.5 * np.cos(
            (np.arange(low, high + 1) - index) / tail_size * np.pi
        )

        return np.average(series[low : high + 1], weights=weights)
