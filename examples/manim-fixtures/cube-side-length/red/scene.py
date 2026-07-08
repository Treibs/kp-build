from manim import *


class CubeSizeKwarg(ThreeDScene):
    def construct(self):
        cube = Cube(size=1.5, fill_opacity=0.75)
        self.add(cube)
        self.wait(0.5)
