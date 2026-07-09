from manim import *
import numpy as np


class ImagesInVGroup(Scene):
    def construct(self):
        arr = np.zeros((8, 8, 4), dtype=np.uint8)
        arr[2:6, 2:6] = [200, 40, 40, 255]
        # VGroup only accepts vectorized mobjects; ImageMobject is not one
        row = VGroup(ImageMobject(arr), ImageMobject(arr))
        self.add(row)
        self.wait(0.2)
