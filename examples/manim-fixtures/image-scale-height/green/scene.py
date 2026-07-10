from manim import *
import numpy as np


class SizedSprite(Scene):
    def construct(self):
        # size an image in scene units with the height property (or
        # scale_to_fit_height) — .scale(n) is a multiplier on the image's
        # native pixel size, not a target height, and a 16px sprite
        # "scaled to 1.5" renders as a near-invisible speck
        arr = np.zeros((8, 8, 4), dtype=np.uint8)
        arr[2:6, 2:6] = [200, 40, 40, 255]
        sprite = ImageMobject(arr)
        sprite.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        sprite.height = 2
        self.add(sprite)
        self.wait(0.2)
