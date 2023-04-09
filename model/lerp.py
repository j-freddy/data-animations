import numpy as np
import math

class Lerp:
    @staticmethod
    def linear(arr, index: float):
        before = arr[int(index)]
        after = arr[min(len(arr) - 1, int(index) + 1)]
        return np.interp(index % 1.0, [0, 1], [before, after])

    @staticmethod
    def weighted_avg(arr, index: float, kernel_size):
        assert kernel_size % 2 == 1

        tail_size = kernel_size // 2

        low = int(max([0, np.ceil(index - tail_size)]))
        high = int(min([len(arr) - 1, np.floor(index + tail_size)]))

        weights = 0.5 + 0.5 * np.cos(
            (np.arange(low, high + 1) - index) / tail_size * np.pi
        )

        return np.average(arr[low:high + 1], weights=weights)
