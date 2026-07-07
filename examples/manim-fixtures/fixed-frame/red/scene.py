from manim import *


class FixInFrameTitle(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        title = Text("Surface", font_size=24)
        title.fix_in_frame()
        title.to_corner(UL)
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(axes, title)
        self.play(FadeIn(title), run_time=0.5)
