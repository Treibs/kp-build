from manim import *


class DrawCircle(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        self.play(Create(circle), run_time=0.5)
