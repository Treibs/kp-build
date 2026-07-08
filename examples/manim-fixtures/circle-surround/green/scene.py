from manim import *


class SurroundBox(Scene):
    def construct(self):
        square = Square(side_length=1.5)
        ring = Circle().surround(square, buffer_factor=1.4)
        self.add(square)
        self.play(Create(ring), run_time=0.5)
