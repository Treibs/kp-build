from manim import *
import numpy as np


class CrispSprite(Scene):
    def construct(self):
        # a tiny pixel-art swatch as a raw array; no asset file needed
        arr = np.zeros((8, 8, 4), dtype=np.uint8)
        arr[1:4, 2:6] = [240, 195, 150, 255]
        arr[4:7, 1:7] = [200, 40, 40, 255]
        sprite = ImageMobject(arr)
        # hard pixel edges when scaled up: nearest-neighbor resampling
        sprite.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        sprite.height = 4
        self.add(sprite)
        self.wait(0.2)
