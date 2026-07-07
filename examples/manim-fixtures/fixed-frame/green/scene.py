from manim import *


class FixedFrameTitle(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        title = Text("Surface", font_size=24).to_corner(UL)
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(axes), run_time=0.5)
