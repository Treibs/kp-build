from manim import *


class SurroundBoxBuff(Scene):
    def construct(self):
        square = Square(side_length=1.5)
        ring = Circle()
        ring.surround(square, buffer=0.3)
        self.add(square, ring)
