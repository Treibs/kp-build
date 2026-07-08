from manim import *


class TopDownToSideOn(ThreeDScene):
    def construct(self):
        cube = Cube(side_length=1.5, fill_opacity=0.75)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)
        self.add(cube)
        self.move_camera(phi=90 * DEGREES, run_time=0.5)
