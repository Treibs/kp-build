from manim import *


class TrackerDrivesAngle(Scene):
    def construct(self):
        tracker = ValueTracker(0)
        line = always_redraw(
            lambda: Line(ORIGIN, RIGHT * 2).rotate(tracker.get_value(), about_point=ORIGIN))
        self.add(line)
        self.play(tracker.animate.set_value(PI / 2), run_time=0.5)
