import numpy as np

class Utils:
    @staticmethod
    def get_random_color(presentation=False):
        # presentation=True means we generate colours not too dark or light
        # (i.e. colours used for a presentation)
        low = 64 if presentation else 0
        high = 191 if presentation else 255

        color = np.random.randint(low, high, size=3)
        return tuple(color)
