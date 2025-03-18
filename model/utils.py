import argparse
import numpy as np

from model.const import (
    FILE_IN_DEFAULT,
    FILE_OUT_DEFAULT,
    NUM_VISIBLE_DEFAULT,
    TITLE_DEFAULT,
)
from view.const import FRAMES_PER_TIMESTAMP_DEFAULT, PROD_DEFAULT


class Utils:
    @staticmethod
    def get_random_color(presentation: bool = True) -> tuple[int, int, int]:
        """
        Generate a random RGB color.

        Args:
            presentation (bool, optional): If True, generates colors that are
                not too light nor too dark, i.e. colours used for a
                presentation. Default: True.

        Returns:
            tuple[int, int, int]: A tuple representing an RGB color, where each
                component is an integer strictly within the range [0, 255].
        """

        # presentation=True means we generate colours not too dark or light
        # (i.e. colours used for a presentation)
        low = 64 if presentation else 0
        high = 191 if presentation else 255

        color = np.random.randint(low, high, size=3)
        return tuple(color)

    @staticmethod
    def parse_args() -> tuple[str, str, float, int, bool, str]:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-data",
            type=str,
            help=f"Input data filename (without extension). Must be .csv and reside in data/. Default: {FILE_IN_DEFAULT}",
            default=FILE_IN_DEFAULT,
        )
        parser.add_argument(
            "-title",
            type=str,
            help=f"Title displayed in video. (default: {TITLE_DEFAULT})",
            default=TITLE_DEFAULT,
        )
        parser.add_argument(
            "-fpe",
            type=float,
            help=f"Frames per timestamp. A larger value results in slower animation. Default: {FRAMES_PER_TIMESTAMP_DEFAULT}",
            default=FRAMES_PER_TIMESTAMP_DEFAULT,
        )
        parser.add_argument(
            "-visible",
            type=int,
            help=f"Number of top visible series. Default: {NUM_VISIBLE_DEFAULT}",
            default=NUM_VISIBLE_DEFAULT,
        )
        parser.add_argument(
            "-prod",
            action=argparse.BooleanOptionalAction,
            help=f"If True, enter production mode to record and save animation as .mp4 file. Default: {PROD_DEFAULT}",
            default=PROD_DEFAULT,
        )
        parser.add_argument(
            "-out",
            type=str,
            help=f"If in production mode, specifies output filename (without extension). Default: {FILE_OUT_DEFAULT}",
            default=FILE_OUT_DEFAULT,
        )

        args = parser.parse_args()

        return args.data, args.title, args.fpe, args.visible, args.prod, args.out
