from manim import *


class EasedSlide(Scene):
    def construct(self):
        # rate functions are module members with qualified names:
        # ease_out_sine / ease_in_sine etc. — there is no bare `ease_out`
        dot = Dot(LEFT * 3)
        self.add(dot)
        self.play(dot.animate.shift(RIGHT * 6), rate_func=rate_functions.ease_out_sine, run_time=0.5)
