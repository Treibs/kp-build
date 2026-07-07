from manim import *


class DrawCircleOldName(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        self.play(ShowCreation(circle), run_time=0.5)
