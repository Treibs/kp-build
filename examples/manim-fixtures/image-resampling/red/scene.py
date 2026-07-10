from manim import *
import numpy as np


class BlurKwarg(Scene):
    def construct(self):
        # there is no PIL/scipy-style filtering kwarg on ImageMobject;
        # crispness is set via set_resampling_algorithm (see green)
        arr = np.zeros((8, 8, 4), dtype=np.uint8)
        arr[2:6, 2:6] = [200, 40, 40, 255]
        sprite = ImageMobject(arr, filter_kwargs={"order": 0})
        self.add(sprite)
        self.wait(0.2)
