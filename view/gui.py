import pyglet
from pyglet import shapes
import sys

from view.bar_plot import BarPlot
from view.const import FPS, FRAMES_PER_ENTRY, GLOBAL_SCALE, PROD, WINDOW_H, WINDOW_W

class GUI:
    def __init__(self, data_handler):
        self.data_handler = data_handler

        self.window = pyglet.window.Window(self.w(), self.h())

        padding = 16 * GLOBAL_SCALE
        self.plot = BarPlot(
            data_handler,
            x=padding,
            y=padding,
            width=self.w() - padding * 2,
            height=self.h(),
        )

        # self.frames is only used for calculating self.entry_index which is a
        # float
        self.frames: float = 0

        self.batch = pyglet.graphics.Batch()
        self.initialise_sprites()
    
    def w(self):
        return WINDOW_W * GLOBAL_SCALE

    def h(self):
        return WINDOW_H * GLOBAL_SCALE
    
    def initialise_sprites(self):
        self.sprites_base = shapes.Rectangle(0, 0, self.w(), self.h(), color=(33, 37, 41), batch=self.batch)

    def draw_background(self):
        self.batch.draw()
    
    def update(self, dt):
        self.entry_index: float = self.frames / FRAMES_PER_ENTRY + 520

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
            self.draw_background()
            self.plot.draw(self.data_handler, self.entry_index)
        
        pyglet.clock.schedule_interval(self.update, 1 / FPS)
        pyglet.app.run()
