import imageio.v2 as iio
import os
import numpy as np
import pyglet
from pyglet import shapes

from model.const import DIR_OUT
from model.data_handler import DataHandler
from view.bar_plot import BarPlot
from view.const import (
    FPS,
    WINDOW_H,
    WINDOW_W,
)


class GUI:
    """
    noqa
    """

    def __init__(
        self,
        data_handler,
        title_label,
        frames_per_entry=2.5,
        num_visible=10,
        prod=False,
        file_out=None,
    ):
        self.data_handler: DataHandler = data_handler

        self.title_label = title_label
        self.frames_per_entry = frames_per_entry
        self.prod = prod
        # Local screen is too small for 1920x1080
        self.scale = 1 if prod else 0.5
        self.window = pyglet.window.Window(self.w(), self.h())

        padding = 16 * self.scale

        self.plot = BarPlot(
            data_handler,
            x=padding,
            y=padding,
            width=self.w() - padding * 2,
            height=self.h() * 0.85,
            num_visible=num_visible,
            prod=prod,
        )

        # self.frames is only used for calculating self.entry_index which is a
        # float
        self.frames: float = 0

        if prod:
            if not os.path.exists(DIR_OUT):
                os.makedirs(DIR_OUT)

            self.writer = iio.get_writer(
                os.path.join(DIR_OUT, f"{file_out}.mp4"), fps=FPS
            )

        self.batch_background = pyglet.graphics.Batch()
        self.batch_foreground = pyglet.graphics.Batch()
        self.initialise_sprites()

    def w(self):
        return int(WINDOW_W * self.scale)

    def h(self):
        return int(WINDOW_H * self.scale)

    def initialise_sprites(self):
        self.sprites_base = shapes.Rectangle(
            0, 0, self.w(), self.h(), color=(33, 37, 41), batch=self.batch_background
        )

        padding = 8 * self.scale

        # Edit title here
        self.sprites_title = pyglet.text.Label(
            self.title_label,
            font_name="Impact",
            font_size=36 * self.scale,
            x=self.w() / 2,
            y=self.h() * 0.85 + padding,
            anchor_x="center",
            anchor_y="bottom",
            batch=self.batch_foreground,
        )

        padding = 48 * self.scale

        # Date time
        self.sprites_time = pyglet.text.Label(
            font_name="Impact",
            font_size=48 * self.scale,
            # Anchor left otherwise year on the date jitters
            # Unfortunately this means we have to guess the width of the text
            x=self.w() - padding - 288 * self.scale,
            y=padding,
            anchor_x="left",
            anchor_y="bottom",
            batch=self.batch_foreground,
        )

    def capture_frame(self):
        color_buffer = pyglet.image.get_buffer_manager().get_color_buffer()

        image_data = color_buffer.get_image_data()
        buffer = image_data.get_data("RGBA", image_data.pitch)

        # 4 channels: RGBA
        frame = np.asarray(buffer).reshape((image_data.height, image_data.width, 4))
        # Make image correctly oriented
        frame = np.flipud(frame)

        self.writer.append_data(frame)

    def update(self, dt):
        entry_index = self.frames / self.frames_per_entry

        # Stop if end reached
        if entry_index >= self.data_handler.num_series():
            pyglet.clock.unschedule(self.update)
            if self.prod:
                self.writer.close()
            self.window.close()
            return

        self.entry_index: float = entry_index

        # Update background
        self.sprites_time.text = self.data_handler.get_timestamp(int(self.entry_index))

        # Go to next frame
        if self.prod:
            # During production we create a snapshot of each frame
            self.frames += 1
        else:
            # During development we take care of frame drops
            self.frames += dt * FPS

    def run(self):
        @self.window.event
        def on_draw():
            self.window.clear()
            self.batch_background.draw()
            self.plot.draw(self.data_handler, self.entry_index)
            self.batch_foreground.draw()

            # Capture frame during production
            if self.prod:
                self.capture_frame()

        pyglet.clock.schedule_interval(self.update, 1 / FPS)
        pyglet.app.run()
