import pyglet
from pyglet import shapes
import sys

from model.data_handler import DataHandler
from view.bar_plot import BarPlot
from view.const import FPS, FRAMES_PER_ENTRY, GLOBAL_SCALE, PROD, WINDOW_H, WINDOW_W

class GUI:
    def __init__(self, data_handler):
        self.data_handler: DataHandler = data_handler

        self.window = pyglet.window.Window(self.w(), self.h())

        padding = 16 * GLOBAL_SCALE
        self.plot = BarPlot(
            data_handler,
            x=padding,
            y=padding,
            width=self.w() - padding * 2,
            height=self.h() * 0.85,
        )

        # self.frames is only used for calculating self.entry_index which is a
        # float
        self.frames: float = 0

        self.batch_background = pyglet.graphics.Batch()
        self.batch_foreground = pyglet.graphics.Batch()
        self.initialise_sprites()
    
    def w(self):
        return WINDOW_W * GLOBAL_SCALE

    def h(self):
        return WINDOW_H * GLOBAL_SCALE
    
    def initialise_sprites(self):
        self.sprites_base = shapes.Rectangle(0, 0, self.w(), self.h(), color=(33, 37, 41), batch=self.batch_background)

        padding = 8 * GLOBAL_SCALE

        # Edit title here
        self.sprites_title = pyglet.text.Label(
            "IQs over time",
            font_name="Impact",
            font_size=36 * GLOBAL_SCALE,
            x=self.w() / 2,
            y=self.h() * 0.85 + padding,
            anchor_x="center",
            anchor_y="bottom",
            batch=self.batch_foreground,
        )

        padding = 48 * GLOBAL_SCALE

        # Date time
        self.sprites_time = pyglet.text.Label(
            font_name="Impact",
            font_size=48 * GLOBAL_SCALE,
            # Anchor left otherwise year on the date jitters
            # Unfortunately this means we have to guess the width of the text
            x=self.w() - padding - 288,
            y=padding,
            anchor_x="left",
            anchor_y="bottom",
            batch=self.batch_foreground,
        )
    
    def update(self, dt):
        entry_index = self.frames / FRAMES_PER_ENTRY

        # Stop if end reached
        if entry_index >= self.data_handler.num_entries():
            pyglet.clock.unschedule(self.update)
            return
    
        self.entry_index: float = entry_index

        # Update background
        self.sprites_time.text = self.data_handler.get_time(int(self.entry_index))

        # Go to next frame
        if PROD:
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
        
        pyglet.clock.schedule_interval(self.update, 1 / FPS)
        pyglet.app.run()
