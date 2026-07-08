from manim import *


class DistanceKwargSwallowed(ThreeDScene):
    def construct(self):
        cube = Cube(side_length=1.5, fill_opacity=0.75)
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES, distance=99)
        self.add(cube)
        self.wait(0.5)
