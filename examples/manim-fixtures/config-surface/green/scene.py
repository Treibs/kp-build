from manim import *


class ConfigFrameWidth(Scene):
    def construct(self):
        bar = Rectangle(width=config.frame_width - 1, height=0.5, color=GREEN)
        self.play(Create(bar), run_time=0.5)
