from manim import *


class CameraZoomIn(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        cube = Cube(side_length=1.5, fill_opacity=0.75)
        self.add(cube)
        self.move_camera(zoom=2, run_time=0.5)
