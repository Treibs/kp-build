from manim import *
import numpy as np


class ImagesInGroup(Scene):
    def construct(self):
        arr = np.zeros((8, 8, 4), dtype=np.uint8)
        arr[2:6, 2:6] = [200, 40, 40, 255]
        # image mobjects group with Group (VGroup is vector-only)
        row = Group(ImageMobject(arr), ImageMobject(arr), Text("x2"))
        row.arrange(RIGHT, buff=0.5)
        self.add(row)
        self.wait(0.2)
