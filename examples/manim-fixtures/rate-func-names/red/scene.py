from manim import *


class BareEase(Scene):
    def construct(self):
        # `ease_out` alone names nothing (see green for the real names)
        dot = Dot(LEFT * 3)
        self.add(dot)
        self.play(dot.animate.shift(RIGHT * 6), rate_func=ease_out, run_time=0.5)
