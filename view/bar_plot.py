import math
import numpy as np
import pyglet
from pyglet import shapes

from model.data_handler import DataHandler
from model.lerp import Lerp
from model.utils import Utils
from view.const import RANK_LERP_KERNEL_SIZE

class BarPlot:
    def __init__(self, data_handler: DataHandler, x, y, width, height, num_visible=10, prod=False):
        self.x = x
        self.y = y
        self.width = width
        self.full_height = height

        self.num_visible = num_visible

        # Make space for axis labels
        self.scale = 1 if prod else 0.5
        self.height = self.full_height - 64 * self.scale

        self.bar_height = 0.75 * self.height / self.num_visible

        # Cache order of data features
        self.data_features = data_handler.features.values()

        self.batch_tick = pyglet.graphics.Batch()
        self.batch = pyglet.graphics.Batch()
        self.initialise_sprites()

    def value_to_x(self, value, max_value):
        return self.x + self.width * value / max_value

    def rank_to_y(self, rank):
        return self.y + (self.num_visible - rank - 1) * self.height / self.num_visible

    def initialise_sprites(self):
        self.sprites_bars = []
        self.sprites_labels = []

        for feature in self.data_features:
            bar = shapes.Rectangle(
                0, 0, 0, 0,
                color=Utils.get_random_color(presentation=True),
                batch=self.batch,
            )

            label = pyglet.text.Label(
                feature.id,
                font_name="Impact",
                font_size=self.bar_height * 0.5,
                anchor_x="right",
                anchor_y="bottom",
                batch=self.batch,
            )

            self.sprites_bars.append(bar)
            self.sprites_labels.append(label)
    
    def update_bars(self, entry_index: float, max_value):
        for i, feature in enumerate(self.data_features):
            rank = Lerp.weighted_avg(feature.ranks, entry_index, kernel_size=RANK_LERP_KERNEL_SIZE)

            # Do not update bars if they are not visible
            if np.linalg.norm(self.num_visible + 1 - rank < 1e-3):
                continue

            value = Lerp.linear(feature.values, entry_index)
            x = self.value_to_x(value, max_value)

            y = self.rank_to_y(rank)

            bar = self.sprites_bars[i]
            bar.x = self.x
            bar.y = y
            bar.width = x - self.x
            bar.height = self.bar_height

            x_padding = 16 * self.scale
            y_padding = 4 * self.scale

            label = self.sprites_labels[i]
            label.x = max(
                x - x_padding,
                self.x + label.content_width + x_padding
            )
            label.y = y + y_padding
    
    def update_ticks(self, data_handler: DataHandler, entry_index: float, max_value):
        # Pyglet needs the sprites but Python garbage collects local variables
        # so this acts as a temporary buffer
        self.sprites_ticks = []

        # TODO Magic number
        unit = Lerp.weighted_avg(data_handler.units_indices, entry_index, 9)
        # Fix floating point errors
        unit = np.round(unit, 3)
        rem = unit % 1.0

        curr = data_handler.available_units[math.floor(unit)]
        next = data_handler.available_units[math.ceil(unit)]

        width = 2 * self.scale
        padding = 8 * self.scale

        def update_tick_at_unit(unit, opacity):
            color = (173, 181, 189, int(opacity))

            for value in range(0, int(max_value), unit):
                x = self.value_to_x(value, max_value)

                tick = shapes.Rectangle(
                    x - width, self.y, width, self.height,
                    color=color,
                    batch=self.batch_tick,
                )

                label = pyglet.text.Label(
                    str(value),
                    font_name="Impact",
                    font_size=24 * self.scale,
                    color=color,
                    x=x,
                    y=self.y + self.height + padding,
                    anchor_x="center",
                    batch=self.batch_tick,
                )

                self.sprites_ticks.append(tick)
                self.sprites_ticks.append(label)
        
        # TODO Make util function or just clean up
        update_tick_at_unit(curr, 255 - rem * 255)
        update_tick_at_unit(next, rem * 255)

    def draw(self, data_handler: DataHandler, entry_index: float):
        max_value = data_handler.get_max_bar_width(entry_index)

        self.update_ticks(data_handler, entry_index, max_value)
        self.update_bars(entry_index, max_value)

        self.batch_tick.draw()
        self.batch.draw()
