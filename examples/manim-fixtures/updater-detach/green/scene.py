from manim import *


class DetachThenAnimate(Scene):
    def construct(self):
        tracker = ValueTracker(0)
        counter = DecimalNumber(0, num_decimal_places=0)
        live = lambda m: m.set_value(tracker.get_value())
        counter.add_updater(live)
        self.add(counter)
        self.play(tracker.animate.set_value(100), run_time=0.5)
        counter.remove_updater(live)
        self.play(counter.animate.shift(RIGHT * 2), run_time=0.5)
