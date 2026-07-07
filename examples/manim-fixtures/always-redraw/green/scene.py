from manim import *


class AlwaysRedrawLabel(Scene):
    def construct(self):
        tracker = ValueTracker(0)
        dot = always_redraw(lambda: Dot(RIGHT * tracker.get_value(), color=YELLOW))
        label = always_redraw(
            lambda: DecimalNumber(tracker.get_value(), num_decimal_places=1).next_to(dot, UP))
        self.add(dot, label)
        self.play(tracker.animate.set_value(2), run_time=0.5)
