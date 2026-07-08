from manim import *


class ThreeDFrameZoom(ThreeDScene):
    def construct(self):
        cube = Cube(side_length=1.5, fill_opacity=0.75)
        self.add(cube)
        self.play(self.camera.frame.animate.scale(0.5))
